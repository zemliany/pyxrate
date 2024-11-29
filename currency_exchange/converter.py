from typing import Optional
from dataclasses import dataclass, field
from currency_exchange.data import ExchangeApiClient
from currency_exchange.logger import LoggerConfig, LogLevel
from currency_exchange.exceptions import CurrencyAmountValueError, CurrencyTypeError


@dataclass
class CurrencyConverter(ExchangeApiClient):
    currencies_endpoint: str = field(default='/currencies/')

    def __post_init__(self):
        self.logger_config = LoggerConfig(name="CurrencyConverter", level=LogLevel.NOTSET)
        self.logger = self.logger_config.get_logger()

    def _args_to_lowercase(func):
        """
        Simple decorator to make argument names lowercase.
        """

        def wrapper(*args, **kwargs):
            make_lowercase = lambda x: x.lower() if isinstance(x, str) else x
            new_args = tuple(map(make_lowercase, args))
            new_kwargs = {k: make_lowercase(v) for k, v in kwargs.items()}
            return func(*new_args, **new_kwargs)

        return wrapper

    def validate_amount(func):
        """
        Decorator to validate that the first positional argument (amount) is an int or float.
        """

        def wrapper(*args, **kwargs):
            # Assume the currency_amount is the first positional argument after self
            if len(args) > 1:
                currency_amount = args[1]
                if not isinstance(currency_amount, (int, float)):
                    raise CurrencyTypeError(type(currency_amount).__name__)
                if currency_amount <= 0:
                    raise CurrencyAmountValueError(amount=currency_amount)
            return func(*args, **kwargs)

        return wrapper

    @property
    def log_level(self) -> LogLevel:
        return self.logger_config.log_level

    @log_level.setter
    def log_level(self, level: LogLevel | str):
        """
        Set the log level dynamically using LoggerConfig.
        """
        self.logger_config.log_level = level

    @_args_to_lowercase
    def currencies(self, currency_code: Optional[str] = None):
        """
        :param currency_code: represents shortname of currency, e.g UAH, USD, EUR
        :return: dict: supported currencies from API
        """
        all_currencies = self.get("/currencies.json")
        if isinstance(currency_code, str):
            self.logger.debug(f"Get currency name for code: {currency_code.upper()}")
            try:
                all_currencies[currency_code]
            except KeyError:
                raise KeyError(f"{currency_code} is not a valid currency code or currency code is not supported")
            return all_currencies[currency_code]
        else:
            self.logger.debug("Retrieving all supported currencies API call")
            self.logger.debug(f"All supported currencies names: {all_currencies}")
        return all_currencies

    @_args_to_lowercase
    def get_exchange_rate(self, currency_to_exchange: str, currency_to_get: str):
        self.logger.debug(f"Currency for exchange: {currency_to_exchange.upper()}")
        self.logger.debug(f"Currency to retrieve: {currency_to_get.upper()}")
        endpoint = f"{self.currencies_endpoint}{currency_to_exchange}.json"
        self.logger.debug(f"Exchange endpoint API for exchange operation: {endpoint}")
        rate_data = self.get(endpoint)
        self.logger.debug(
            f"All exchange currencies rates for {currency_to_exchange.upper()} sell at "
            f"{rate_data['date']}: {rate_data[currency_to_exchange]}"
        )
        self.logger.debug(
            f"Exchange rate from {currency_to_exchange.upper()} to {currency_to_get.upper()}: "
            f"{ rate_data[currency_to_exchange][currency_to_get]}"
        )
        return rate_data[currency_to_exchange][currency_to_get]

    @validate_amount
    def convert(self, currency_amount: float, currency_to_exchange: str, currency_to_get: str) -> float:
        rate = self.get_exchange_rate(currency_to_exchange, currency_to_get)
        exchange_result = round(currency_amount * rate, 2)
        self.logger.debug(
            f"Exchange operation: {currency_to_exchange.upper()} => {currency_to_get.upper()} "
            f"| Currency to sell: {currency_to_exchange.upper()} | Currency to buy: {currency_to_get.upper()} "
            f"| Currency amount: {currency_amount} | Rate: {rate}"
        )
        self.logger.debug(
            f"Exchange operation: {currency_to_exchange.upper()} => {currency_to_get.upper()}: {exchange_result}"
        )
        return exchange_result
