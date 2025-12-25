def validate_value(value: float) -> None:
    if value is None:
        raise ValueError("Value is None")

    if value < 0:
        raise ValueError("Negative values are not allowed")
