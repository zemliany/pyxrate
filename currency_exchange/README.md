# Python Currency Exchange Library

Currency Exchange Rate Library is a lightweight Python package for retrieving and using foreign exchange rates. 
It leverages the [Exchange API by Fawaz Ahmed](https://github.com/fawazahmed0/exchange-api) to provide up-to-date and historical exchange rates in a simple, 
developer-friendly manner.

### Features:
* Real-Time Exchange Rates: Fetch the latest exchange rates for any supported currency pair.
* Historical Data: Retrieve exchange rates for any given date.
* Easy Integration: Simple and intuitive API for seamless integration.
* Case-insensitive currency codes support
* Developed with Asynchronous approach with AsyncIO and AIOHTTP
* High Accuracy: Powered by the reliable Exchange API.
* Open Source: Licensed under MIT for community contributions and customizations.

### Installation

```bash
pip3 install pyxrate
```

### Dependencies
* Python <4.0, >=3.11
* aiohttp

### Quick Start

```python
from currency_exchange import converter

# Initialize the library
currency_client = converter.CurrencyConverter()

# Get the supported currency rates
all_currencies = currency_client.currencies()
print(f"All supported currencies: {all_currencies}")

# Check support of specific currency rate
# NOTE: currency codes are case-insensitive
currency = currency_client.currencies('uah')
print(f"Currency name: {currency}")

currency = currency_client.currencies('UAH')  
print(f"Currency name: {currency}")

# Get exchange rate between two currencies
# NOTE: currency codes are case-insensitive
rate = currency_client.get_exchange_rate('USD', 'UAH')
print(f"USD to UAH rate: {rate}")

rate = currency_client.get_exchange_rate('usd', 'uah')
print(f"USD to UAH rate: {rate}")

# Get historical exchange rate between two currencies for particular date
# NOTE: currency codes are case-insensitive
currency_client.currency_date = '2024-11-20'
historical_rate = currency_client.get_exchange_rate('USD', 'UAH')
print(f"USD to UAH rate at {currency_client.currency_date}: {historical_rate}")

# Convert currencies based on latest rates
# NOTE: currency codes are case-insensitive
currency_convert = currency_client.convert(2400, 'usd', 'uah')
print(f"Convert USD to UAH: {currency_convert}")

# Convert currencies by rates based on historical data
# NOTE: currency codes are case-insensitive
currency_client.currency_date = '2024-11-20'
currency_convert = currency_client.convert(2400, 'usd', 'uah')
print(f"Converting USD to UAH at {currency_client.currency_date} date: {currency_convert}")
```

### Debug mode

```python
from currency_exchange import converter

# Initialize the library
currency_client = converter.CurrencyConverter()

# Set log level to debug
currency_client.log_level = "DEBUG"

# Convert currencies by rates based on historical data
currency_client.currency_date = '2024-11-20'
currency_convert = currency_client.convert(2400, 'usd', 'uah')
print(f"Converting USD to UAH at {currency_client.currency_date} date: {currency_convert}")
```

### Known Issues and Limitations

* Historical Data Availability: **The Exchange API provides historical exchange rate data only up to March 2, 2024**. 
Any requests for dates beyond this range may result in throwing exceptions expected. So, within that, please be 
notified that **all exchange operations by using this lib in terms of historical data limited by date of March 2, 2024**

### Acknowledgments
* Thanks to Fawaz Ahmed for the amazing [Exchange API](https://github.com/fawazahmed0/exchange-api).
* Much appreciated to [SET University](https://www.setuniversity.edu.ua/en/) in scope of which this library was 
developed as part of final project for Python course as part of Master's deegree program for [ML & Cloud Computing](https://www.setuniversity.edu.ua/en/education/computer-science-machine-learning-cloud-computing/)
* Big kudos to tutor and mentor [Denys Kotov](https://www.linkedin.com/in/deniskkotov/)
