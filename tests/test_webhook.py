"""Gumroad webhook handler tests — all use synthetic payloads (no network)."""

from core.refresh_token import verify_token
from core.webhook import (
    DEFAULT_PRODUCT_TO_NICHE,
    WebhookResult,
    handle_gumroad_ping,
)


SECRET = "shared-webhook-secret"
PACK_SECRET = "pack-refresh-secret"


def _valid_payload(**overrides) -> dict:
    """Build a minimal valid Gumroad Ping payload."""
    base = {
        "email": "buyer@example.com",
        "permalink": "pickaxe-crypto",
        "seller_id": "my-gumroad-id",
        "sale_id": "abc123",
    }
    base.update(overrides)
    return base


def test_rejects_missing_submitted_secret():
    r = handle_gumroad_ping(_valid_payload(),
                            shared_secret=SECRET, submitted_secret="",
                            pack_secret=PACK_SECRET)
    assert not r.ok and "secret" in r.reason


def test_rejects_wrong_submitted_secret():
    r = handle_gumroad_ping(_valid_payload(),
                            shared_secret=SECRET, submitted_secret="wrong",
                            pack_secret=PACK_SECRET)
    assert not r.ok and r.reason == "wrong webhook secret"


def test_rejects_missing_email():
    payload = _valid_payload(email="")
    r = handle_gumroad_ping(payload, shared_secret=SECRET, submitted_secret=SECRET,
                            pack_secret=PACK_SECRET)
    assert not r.ok and "email" in r.reason


def test_rejects_invalid_email():
    payload = _valid_payload(email="notanemail")
    r = handle_gumroad_ping(payload, shared_secret=SECRET, submitted_secret=SECRET,
                            pack_secret=PACK_SECRET)
    assert not r.ok


def test_rejects_unknown_product():
    payload = _valid_payload(permalink="unknown-product-slug")
    r = handle_gumroad_ping(payload, shared_secret=SECRET, submitted_secret=SECRET,
                            pack_secret=PACK_SECRET)
    assert not r.ok and "unknown product" in r.reason
    # email survives for logging
    assert r.email == "buyer@example.com"


def test_rejects_seller_id_mismatch_when_pinned():
    payload = _valid_payload(seller_id="some-other-seller")
    r = handle_gumroad_ping(payload, shared_secret=SECRET, submitted_secret=SECRET,
                            pack_secret=PACK_SECRET,
                            expected_seller_id="my-gumroad-id")
    assert not r.ok and "seller_id" in r.reason


def test_seller_id_check_skipped_when_not_pinned():
    payload = _valid_payload(seller_id="anything")
    r = handle_gumroad_ping(payload, shared_secret=SECRET, submitted_secret=SECRET,
                            pack_secret=PACK_SECRET)
    assert r.ok


def test_issues_valid_token_on_clean_payload():
    payload = _valid_payload()
    r = handle_gumroad_ping(payload, shared_secret=SECRET, submitted_secret=SECRET,
                            pack_secret=PACK_SECRET)
    assert r.ok
    assert r.email == "buyer@example.com"
    assert r.niche == "crypto_trading"
    assert r.token is not None
    # Token must verify with the same pack_secret
    payload_decoded = verify_token(r.token, PACK_SECRET)
    assert payload_decoded is not None
    assert payload_decoded.email == "buyer@example.com"
    assert payload_decoded.niche == "crypto_trading"


def test_email_sender_called_with_token_in_body():
    captured = []
    def sender(to: str, subject: str, body: str) -> None:
        captured.append((to, subject, body))
    payload = _valid_payload()
    r = handle_gumroad_ping(
        payload, shared_secret=SECRET, submitted_secret=SECRET,
        pack_secret=PACK_SECRET, email_sender=sender,
    )
    assert r.ok
    assert len(captured) == 1
    to, subj, body = captured[0]
    assert to == "buyer@example.com"
    assert "crypto_trading" in subj.lower()
    assert r.token in body
    assert "Pack_Refresh" in body


def test_email_send_failure_does_not_block_token_issue():
    """If email sending raises, we still consider the webhook OK and return the token —
    the seller can manually resend later."""
    def bad_sender(to: str, subject: str, body: str) -> None:
        raise RuntimeError("SMTP timeout")
    payload = _valid_payload()
    r = handle_gumroad_ping(
        payload, shared_secret=SECRET, submitted_secret=SECRET,
        pack_secret=PACK_SECRET, email_sender=bad_sender,
    )
    assert r.ok
    assert r.token is not None
    assert "send failed" in r.reason


def test_missing_pack_secret_fails_clearly():
    payload = _valid_payload()
    r = handle_gumroad_ping(payload, shared_secret=SECRET, submitted_secret=SECRET,
                            pack_secret="")
    assert not r.ok and "PACK_REFRESH_SECRET" in r.reason


def test_custom_product_mapping_overrides_default():
    payload = _valid_payload(permalink="my-custom-slug")
    r = handle_gumroad_ping(
        payload, shared_secret=SECRET, submitted_secret=SECRET,
        pack_secret=PACK_SECRET,
        product_to_niche={"my-custom-slug": "ai_engineering"},
    )
    assert r.ok and r.niche == "ai_engineering"


def test_email_is_normalized_to_lowercase_trimmed():
    payload = _valid_payload(email="  BUYER@Example.COM  ")
    r = handle_gumroad_ping(
        payload, shared_secret=SECRET, submitted_secret=SECRET,
        pack_secret=PACK_SECRET,
    )
    assert r.ok and r.email == "buyer@example.com"


def test_all_three_packs_resolvable_via_default_mapping():
    """All currently-shipped packs must have at least one Gumroad slug in the default map."""
    niches_in_default = set(DEFAULT_PRODUCT_TO_NICHE.values())
    expected = {"crypto_trading", "ai_engineering", "indie_saas"}
    assert expected.issubset(niches_in_default)


def test_alternate_permalink_field_name_supported():
    """Gumroad sometimes uses 'product_permalink' instead of 'permalink' depending on plan."""
    payload = _valid_payload()
    del payload["permalink"]
    payload["product_permalink"] = "pickaxe-saas"
    r = handle_gumroad_ping(
        payload, shared_secret=SECRET, submitted_secret=SECRET,
        pack_secret=PACK_SECRET,
    )
    assert r.ok and r.niche == "indie_saas"
