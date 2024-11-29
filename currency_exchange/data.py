import asyncio
import aiohttp
from aiohttp.web_exceptions import HTTPError
from dataclasses import dataclass, field
from datetime import datetime
from currency_exchange.logger import LoggerConfig, LogLevel
from currency_exchange.exceptions import CustomDateMismatchException
from aiohttp.client_exceptions import ClientResponseError


@dataclass
class ExchangeApiClient:
    exchange_api: str = field(default='https://cdn.jsdelivr.net/npm/@fawazahmed0/currency-api')
    currency_date: str = field(default='latest')
    api_version: str = field(default='v1')
    headers: dict = field(default_factory=lambda: {"Content-Type": "application/json"})
    logger_config: LoggerConfig = field(init=False)

    def __post_init__(self):
        self.logger_config = LoggerConfig(name="CurrencyConverter", level=LogLevel.NOTSET)
        self.logger = self.logger_config.get_logger()

    @staticmethod
    def check_date(target_date):
        minimal_supported_date = datetime(2024, 3, 2)

        if target_date.year < minimal_supported_date.year:
            raise CustomDateMismatchException(actual_d=target_date)

        if target_date < minimal_supported_date:
            raise CustomDateMismatchException(actual_d=target_date)

    @property
    def log_level(self) -> LogLevel:
        return self.logger_config.log_level

    @log_level.setter
    def log_level(self, level: LogLevel | str):
        self.logger_config.log_level = level

    @property
    def _get_base_url(self) -> str:
        """
          Function that build base_url in proper format for further usage
        :return: str: base_url
        """
        if self.currency_date != 'latest':
            try:
                _date_obj = datetime.strptime(str(self.currency_date), '%Y-%m-%d')
                self.check_date(_date_obj)
            except ValueError:
                raise ValueError(
                    f"Incorrect data format for currency_date {self.currency_date}, "
                    f"allowed formats: 'YEAR-MONTH-DAY' or special value 'latest'. e.g '2024-11-20'"
                )

        base_url = f"{self.exchange_api}@{self.currency_date}/{self.api_version}"
        self.logger.debug(f"Setting currency date to {self.currency_date}")
        self.logger.debug(f"Base url for currency API: {base_url}")
        return base_url

    async def _get(self, endpoint: str, params=None) -> dict:
        """
        Make a GET request to the API.

        Args:
            endpoint (str): API endpoint to call.
            params (dict, optional): Query parameters.
        Returns:
            dict: The JSON response.
        """
        url = f"{self._get_base_url}{endpoint}"
        self.logger.debug(f"Fetching currency data from currency API {url}")
        async with aiohttp.ClientSession(headers=self.headers) as session:
            try:
                async with session.get(url, params=params) as response:
                    response.raise_for_status()
                    return await response.json()
            except (HTTPError, ClientResponseError) as err:
                raise SystemExit(f"{endpoint} not supported", err)

    async def _post(self, endpoint, payload=None):
        """API doesn't support POST requests. Raising NotImplementedError in case of"""
        raise NotImplementedError(f"POST method is not supported for {self._get_base_url}")

    def get(self, endpoint: str, params=None) -> dict:
        return asyncio.run(self._get(endpoint, params))

    def post(self, endpoint: str) -> dict:
        return asyncio.run(self._post(endpoint))
