from outbox_sdk._field_mask import derive_field_mask


def test_basic_fields() -> None:
    result = derive_field_mask({"tags": ["a"], "awareness_enabled": True})
    assert result == ["tags", "awareness_enabled"]


def test_skips_id() -> None:
    result = derive_field_mask({"id": "abc", "tags": ["a"]})
    assert result == ["tags"]


def test_connector_id_is_included() -> None:
    """connector_id is no longer a phantom field — it should be in the mask."""
    result = derive_field_mask({"connector_id": "abc", "tags": ["a"]})
    assert result == ["connector_id", "tags"]


def test_skips_none_values() -> None:
    result = derive_field_mask({"tags": None, "awareness_enabled": True})
    assert result == ["awareness_enabled"]


def test_empty() -> None:
    result = derive_field_mask({"id": "x", "request_id": "y"})
    assert result == []


def test_false_value_is_included() -> None:
    result = derive_field_mask({"require_tls": False})
    assert result == ["require_tls"]


def test_zero_value_is_included() -> None:
    result = derive_field_mask({"page_size": 0})
    assert result == ["page_size"]


def test_empty_list_is_included() -> None:
    result = derive_field_mask({"tags": []})
    assert result == ["tags"]


def test_empty_dict_is_included() -> None:
    result = derive_field_mask({"target_config": {}})
    assert result == ["target_config"]


def test_empty_string_is_included() -> None:
    result = derive_field_mask({"display_name": ""})
    assert result == ["display_name"]
