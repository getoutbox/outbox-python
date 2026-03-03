from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Mapping

_SKIP = frozenset({"id", "request_id"})


def derive_field_mask(input_: Mapping[str, object]) -> list[str]:
    """Derive FieldMask paths from a dict of update fields.

    Skips structural fields (id, request_id) and any key whose value is None.
    For nested dict values (e.g. channel_config or target_config), returns the
    parent key only — not nested paths. This is correct for proto field masks
    which address parent message fields, not leaf scalars.
    """
    return [key for key, value in input_.items() if key not in _SKIP and value is not None]
