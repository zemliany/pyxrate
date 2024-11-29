class CustomDateMismatchException(NotImplementedError):
    """Exception raised when a date's year does not match the expected value."""

    def __init__(self, actual_d, expected_min_m="3", expected_min_y="2024", expected_min_d="2"):
        message = (
            f"Such date for currency operations is not supported by Exchange API: "
            f"minimal expected data that supported by API, "
            f"year: {expected_min_y}, "
            f"month: {expected_min_m}, "
            f"day: {expected_min_d}, "
            f"but got {actual_d}."
        )
        super().__init__(message)
        self.actual_d = actual_d
        self.expected_min_m = expected_min_m
        self.expected_min_y = expected_min_y
        self.expected_min_d = expected_min_d


class CurrencyAmountValueError(ValueError):
    """Exception raised when the currency amount is invalid."""

    def __init__(
        self,
        amount,
        message="currency_amount must be a positive int or float greater than 0",
    ):
        self.amount = amount
        self.message = f"{message}. Got: {amount}"
        super().__init__(self.message)


class CurrencyTypeError(TypeError):
    """Exception raised when the currency amount has an invalid type."""

    def __init__(self, invalid_type, message="currency_amount must be an int or float"):
        self.invalid_type = invalid_type
        self.message = f"{message}. Got: {invalid_type}"
        super().__init__(self.message)
