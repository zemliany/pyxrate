import unittest
from unittest.mock import patch
from currency_exchange.data import ExchangeApiClient
from currency_exchange.converter import CurrencyConverter
from currency_exchange.exceptions import (
    CustomDateMismatchException,
    CurrencyAmountValueError,
    CurrencyTypeError,
)
from datetime import datetime


class TestCurrencyConverter(unittest.TestCase):
    is_class_name_print = False

    def setUp(self):
        """Init the CurrencyConverter instance as part of setup test"""
        if not TestCurrencyConverter.is_class_name_print:
            print(f"Running TestCase: {self.__class__.__name__}")
            TestCurrencyConverter.is_class_name_print = True
        self.converter = CurrencyConverter()
        print(f"Test: {self.id()}")

    @patch.object(ExchangeApiClient, "get")
    def test_get_exchange_rate_invalid_currency_to_exchange(self, mock_get):
        """Test get_exchange_rate with an invalid base currency."""
        # Mock response to simulate API behavior
        mock_get.side_effect = KeyError("foo is not a valid currency code or is not supported")

        # Assert that a KeyError is raised
        with self.assertRaises(KeyError):
            self.converter.get_exchange_rate("foo", "eur")

        mock_get.assert_called_once_with("/currencies/foo.json")

    @patch.object(ExchangeApiClient, "get")
    def test_get_exchange_rate_logging(self, mock_get):
        """Test that appropriate logs are written."""
        mock_response = {
            "usd": {
                "eur": 0.92,
                "gbp": 0.81,
            },
            "date": "2024-11-29",
        }
        mock_get.return_value = mock_response

        with self.assertLogs(self.converter.logger, level="DEBUG") as log:
            self.converter.get_exchange_rate("usd", "eur")
            self.assertIn("Currency for exchange: USD", log.output[0])
            self.assertIn("Currency to retrieve: EUR", log.output[1])
            self.assertIn("Exchange rate from USD to EUR: 0.92", log.output[-1])

    @patch.object(ExchangeApiClient, "get")
    def test_get_exchange_rate_invalid_currency_operational_date_to_exchange(self, mock_get):
        self.converter.currency_date = "2023-11-20"

        mock_get.side_effect = CustomDateMismatchException(
            f"Such date for currency operations is not supported by Exchange API: minimal expected data that "
            f"supported by API, year: 2024, month: 3, day: 2, but got {self.converter.currency_date}."
        )

        # Assert that a KeyError is raised
        with self.assertRaises(CustomDateMismatchException):
            self.converter.get_exchange_rate("foo", "eur")

        mock_get.assert_called_once_with("/currencies/foo.json")

    @patch.object(CurrencyConverter, "get_exchange_rate")
    def test_convert_valid(self, mock_get_exchange_rate):
        """Test the convert method with valid inputs."""
        # Mock the exchange rate
        mock_get_exchange_rate.return_value = 0.92

        # Perform the conversion
        result = self.converter.convert(100, "usd", "eur")

        # Assertions
        self.assertEqual(result, 92.00)  # 100 * 0.92 = 92.00
        mock_get_exchange_rate.assert_called_once_with("usd", "eur")

    @patch.object(CurrencyConverter, "get_exchange_rate")
    def test_convert_invalid_amount(self, mock_get_exchange_rate):
        """Test the convert method with an invalid amount type."""
        # Mock the exchange rate
        mock_get_exchange_rate.return_value = 0.92

        # Test with an invalid type for currency_amount
        with self.assertRaises(CurrencyTypeError) as cm:
            self.converter.convert("invalid_amount", "usd", "eur")
        self.assertIn("currency_amount must be an int or float", str(cm.exception))
        self.assertIn("Got: str", str(cm.exception))

        with self.assertRaises(CurrencyTypeError) as cm:
            self.converter.convert([100], "usd", "eur")
        self.assertIn("currency_amount must be an int or float", str(cm.exception))
        self.assertIn("Got: list", str(cm.exception))

    @patch.object(CurrencyConverter, "get_exchange_rate")
    def test_convert_zero_amount(self, mock_get_exchange_rate):
        """Test the convert method with a zero amount."""
        # Mock the exchange rate
        mock_get_exchange_rate.return_value = 1.2

        # Test with zero amount
        with self.assertRaises(CurrencyAmountValueError) as cm:
            self.converter.convert(0, "usd", "eur")
        self.assertIn(
            "currency_amount must be a positive int or float greater than 0",
            str(cm.exception),
        )
        self.assertIn("Got: 0", str(cm.exception))

    @patch.object(CurrencyConverter, "get_exchange_rate")
    def test_convert_negative_amount(self, mock_get_exchange_rate):
        """Test the convert method with a negative amount."""
        with self.assertRaises(CurrencyAmountValueError) as cm:
            self.converter.convert(-100, "usd", "eur")
        self.assertIn(
            "currency_amount must be a positive int or float greater than 0",
            str(cm.exception),
        )
        self.assertIn("Got: -100", str(cm.exception))


class TestExchangeApiClientInvalidData(unittest.TestCase):
    is_class_name_print = False

    def setUp(self):
        """Init the ExchangeApiClient instance as part of setup test"""
        if not TestExchangeApiClientInvalidData.is_class_name_print:
            print(f"Running TestCase: {self.__class__.__name__}")
            TestExchangeApiClientInvalidData.is_class_name_print = True
        self.api_client = ExchangeApiClient()
        print(f"Test: {self.id()}")

    def test_check_date_valid_date(self):
        """Test scenario for function check_date with a valid date."""
        valid_date = datetime(2024, 3, 3)
        self.api_client.check_date(valid_date)

    def test_check_date_before_minimal_date(self):
        """Test scenario for function check_date with a date before the minimal supported date."""
        invalid_date = datetime(2024, 3, 1)
        with self.assertRaises(CustomDateMismatchException) as cm:
            self.api_client.check_date(invalid_date)
        self.assertIn("2024-03-01", str(cm.exception))

    def test_check_date_year_before_minimal_date(self):
        """Test check_date with a year before the minimal supported date."""
        invalid_date = datetime(2023, 12, 31)
        with self.assertRaises(CustomDateMismatchException) as cm:
            self.api_client.check_date(invalid_date)
        self.assertIn("2023-12-31", str(cm.exception))

    def test_base_url_with_invalid_date(self):
        """Test _get_base_url when invalid date is set."""
        self.api_client.currency_date = "2024-03-01"
        with self.assertRaises(CustomDateMismatchException):
            _ = self.api_client._get_base_url

    def test_base_url_with_invalid_format(self):
        """Test _get_base_url with an invalid date format."""
        self.api_client.currency_date = "invalid-date-format"
        with self.assertRaises(ValueError) as cm:
            _ = self.api_client._get_base_url
        self.assertIn("Incorrect data format for currency_date", str(cm.exception))


class TestCustomDateMismatchException(unittest.TestCase):
    is_class_name_print = False

    def setUp(self):
        if not TestCustomDateMismatchException.is_class_name_print:
            print(f"Running TestCase: {self.__class__.__name__}")
            TestCustomDateMismatchException.is_class_name_print = True
        print(f"Test: {self.id()}")

    def test_exception_message(self):
        actual_date = "2023-12-31"
        expected_min_y = "2024"
        expected_min_m = "3"
        expected_min_d = "2"

        with self.assertRaises(CustomDateMismatchException) as cm:
            raise CustomDateMismatchException(
                actual_d=actual_date,
                expected_min_y=expected_min_y,
                expected_min_m=expected_min_m,
                expected_min_d=expected_min_d,
            )

        exception = cm.exception
        expected_message = (
            f"Such date for currency operations is not supported by Exchange API: minimal expected data that "
            f"supported by API, year: {expected_min_y}, month: {expected_min_m}, day: {expected_min_d}, "
            f"but got {actual_date}."
        )
        self.assertEqual(str(exception), expected_message)

    def test_default_message(self):
        """Test scenario to check default message of CustomDateMismatchException."""
        actual_date = "2023-12-31"

        with self.assertRaises(CustomDateMismatchException) as cm:
            raise CustomDateMismatchException(actual_d=actual_date)

        exception = cm.exception
        expected_message = (
            f"Such date for currency operations is not supported by Exchange API: minimal expected data that "
            f"supported by API, year: 2024, month: 3, day: 2, but got {actual_date}."
        )
        self.assertEqual(str(exception), expected_message)


class TestCurrencyAmountValueError(unittest.TestCase):
    is_class_name_print = False

    def setUp(self):
        if not TestCurrencyAmountValueError.is_class_name_print:
            print(f"Running TestCase: {self.__class__.__name__}")
            TestCurrencyAmountValueError.is_class_name_print = True
        print(f"Test: {self.id()}")

    def test_currency_amount_value_error_default_message(self):
        """Test CurrencyAmountValueError with the default message."""
        amount = -100
        with self.assertRaises(CurrencyAmountValueError) as cm:
            raise CurrencyAmountValueError(amount)
        exception = cm.exception
        self.assertEqual(
            str(exception),
            "currency_amount must be a positive int or float greater than 0. Got: -100",
        )
        self.assertEqual(exception.amount, amount)

    def test_currency_amount_value_error_custom_message(self):
        """Test CurrencyAmountValueError with a custom message."""
        amount = 0
        custom_message = "Custom error message"
        with self.assertRaises(CurrencyAmountValueError) as cm:
            raise CurrencyAmountValueError(amount, custom_message)
        exception = cm.exception
        self.assertEqual(str(exception), f"{custom_message}. Got: {amount}")
        self.assertEqual(exception.amount, amount)
