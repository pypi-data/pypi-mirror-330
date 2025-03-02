def str_to_bool(value: str) -> bool:
    """Convert environment variable string to boolean."""
    return value.lower() in ("true", "1", "yes", "y", "on")