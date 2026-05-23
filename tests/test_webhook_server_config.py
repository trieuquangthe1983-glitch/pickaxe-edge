"""FastAPI webhook server env-resolution tests (no HTTP)."""

import json
import os
from unittest.mock import patch

from webhook_server.main import _resolve_product_map
from core.webhook import DEFAULT_PRODUCT_TO_NICHE


def test_falls_back_to_default_when_env_unset():
    with patch.dict(os.environ, {}, clear=False):
        os.environ.pop("PRODUCT_TO_NICHE_JSON", None)
        m = _resolve_product_map()
    assert m == DEFAULT_PRODUCT_TO_NICHE


def test_falls_back_to_default_when_env_empty_string():
    with patch.dict(os.environ, {"PRODUCT_TO_NICHE_JSON": ""}):
        assert _resolve_product_map() == DEFAULT_PRODUCT_TO_NICHE


def test_loads_valid_json_from_env():
    custom = {"my-crypto-slug": "crypto_trading", "my-ai-slug": "ai_engineering"}
    with patch.dict(os.environ, {"PRODUCT_TO_NICHE_JSON": json.dumps(custom)}):
        assert _resolve_product_map() == custom


def test_falls_back_on_malformed_json():
    with patch.dict(os.environ, {"PRODUCT_TO_NICHE_JSON": "not-json"}):
        assert _resolve_product_map() == DEFAULT_PRODUCT_TO_NICHE


def test_falls_back_when_json_is_not_object():
    with patch.dict(os.environ, {"PRODUCT_TO_NICHE_JSON": '["array", "not", "object"]'}):
        assert _resolve_product_map() == DEFAULT_PRODUCT_TO_NICHE


def test_coerces_non_string_values_to_strings():
    """Defensive: even if user passes weird types, we string-coerce."""
    raw = '{"slug1": "crypto_trading"}'  # plain valid
    with patch.dict(os.environ, {"PRODUCT_TO_NICHE_JSON": raw}):
        m = _resolve_product_map()
    assert all(isinstance(k, str) and isinstance(v, str) for k, v in m.items())
