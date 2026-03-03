from __future__ import annotations


def connector_name(id_: str) -> str:
    return f"connectors/{id_}"


def message_name(id_: str) -> str:
    return f"messages/{id_}"


def account_name(id_: str) -> str:
    return f"accounts/{id_}"


def destination_name(id_: str) -> str:
    return f"destinations/{id_}"


def parse_id(name: str) -> str:
    """Extract the last segment from a resource name."""
    parts = name.split("/")
    if not parts or not parts[-1]:
        msg = f'Invalid resource name: "{name}"'
        raise ValueError(msg)
    return parts[-1]
