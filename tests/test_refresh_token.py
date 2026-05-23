"""HMAC refresh token system tests."""

import pytest

from core.refresh_token import TokenPayload, generate_token, verify_token


SECRET = "test-secret-not-for-production"
NOW = 1_700_000_000  # arbitrary fixed epoch


def test_generate_and_verify_round_trip():
    token = generate_token("buyer@example.com", "crypto_trading", SECRET, now=NOW)
    payload = verify_token(token, SECRET, now=NOW)
    assert payload is not None
    assert payload.email == "buyer@example.com"
    assert payload.niche == "crypto_trading"
    assert payload.issued_at == NOW
    assert payload.expires_at == NOW + 90 * 86400


def test_email_is_lowercased_and_stripped():
    token = generate_token("  BUYER@Example.COM  ", "ai_engineering", SECRET, now=NOW)
    payload = verify_token(token, SECRET, now=NOW)
    assert payload.email == "buyer@example.com"


def test_invalid_email_rejected_at_issue():
    with pytest.raises(ValueError):
        generate_token("notanemail", "crypto_trading", SECRET)


def test_email_with_separator_char_rejected():
    """Pipe is our payload separator — disallow in inputs."""
    with pytest.raises(ValueError):
        generate_token("a|b@example.com", "crypto_trading", SECRET)


def test_niche_with_separator_char_rejected():
    with pytest.raises(ValueError):
        generate_token("a@b.com", "crypto|trading", SECRET)


def test_empty_email_rejected():
    with pytest.raises(ValueError):
        generate_token("", "crypto_trading", SECRET)


def test_empty_secret_rejected_at_issue():
    with pytest.raises(ValueError):
        generate_token("a@b.com", "crypto_trading", "")


def test_token_expires_after_validity_window():
    token = generate_token("a@b.com", "crypto_trading", SECRET, valid_days=30, now=NOW)
    # Just before expiry: valid
    assert verify_token(token, SECRET, now=NOW + 30 * 86400 - 1) is not None
    # Just after expiry: invalid
    assert verify_token(token, SECRET, now=NOW + 30 * 86400 + 1) is None


def test_token_signed_with_different_secret_rejected():
    token = generate_token("a@b.com", "crypto_trading", SECRET, now=NOW)
    assert verify_token(token, "different-secret", now=NOW) is None


def test_tampered_token_rejected():
    token = generate_token("a@b.com", "crypto_trading", SECRET, now=NOW)
    # Flip one character in the middle of the token
    mid = len(token) // 2
    swap = "A" if token[mid] != "A" else "B"
    tampered = token[:mid] + swap + token[mid + 1:]
    assert verify_token(tampered, SECRET, now=NOW) is None


def test_empty_or_garbage_token_returns_none():
    assert verify_token("", SECRET) is None
    assert verify_token("not-base64-and-broken", SECRET) is None
    assert verify_token("YWFhYQ==", SECRET) is None  # valid b64 but wrong format


def test_empty_secret_on_verify_returns_none():
    token = generate_token("a@b.com", "crypto_trading", SECRET, now=NOW)
    assert verify_token(token, "", now=NOW) is None


def test_token_is_url_safe():
    """Tokens must paste safely into URLs / emails (no +, /, or = chars)."""
    token = generate_token("a@b.com", "crypto_trading", SECRET, now=NOW)
    for ch in "+/=":
        assert ch not in token, f"token contains URL-unsafe char {ch!r}"


def test_different_niche_produces_different_token():
    t1 = generate_token("a@b.com", "crypto_trading", SECRET, now=NOW)
    t2 = generate_token("a@b.com", "ai_engineering", SECRET, now=NOW)
    assert t1 != t2


def test_returned_payload_is_immutable():
    """TokenPayload is a frozen dataclass."""
    token = generate_token("a@b.com", "crypto_trading", SECRET, now=NOW)
    payload = verify_token(token, SECRET, now=NOW)
    assert payload is not None
    with pytest.raises(Exception):
        payload.email = "hacker@evil.com"  # type: ignore[misc]
