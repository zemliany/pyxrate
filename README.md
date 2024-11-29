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

Package available in [PyPI](https://pypi.org/project/pyxrate/#description)

Install package via PIP:

```bash
pip3 install pyxrate
```

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

### Setup Environment for development

#### Requirements:
* make
* poetry

#### Make Installation Guideline

**Linux** 

Most Linux distributions come with `make` pre-installed. If it's not available or you need the latest GNU Make version, follow these steps:

**Debian/Ubuntu** 

```bash 
sudo apt update
sudo apt install build-essential
```

**Fedora** 
```bash
sudo dnf install make
```

**CentOS/RHEL**
```bash
sudo yum install make
```

**Arch Linux**
```bash
sudo pacman -S make
```

**Latest GNU Make from Source**

1. Download the latest source from [GNU Make's website](https://ftp.gnu.org/gnu/make/).
2. Extract, configure, and build:

```bash
tar -xvf make-<version>.tar.gz
cd make-<version>
./configure
make
sudo make install
```

**macOS**

macOS typically uses the BSD Make version bundled with Xcode

More details: https://www.gnu.org/software/make/

#### Poetry Installation

Linux, macOS, Windows (WSL) 

```bash
curl -sSL https://install.python-poetry.org | python3 -
```

More details: https://python-poetry.org/docs/#installing-with-the-official-installer

#### Setup development environment

```bash

Available commands:
  help             Show available commands and descriptions
  lock             Generate a new Poetry lock file
  dependencies     Update project dependencies
  env              Set up the development environment
  test             Run unit tests
  format           Format code with Black
  lint             Lint the codebase
  patch            Increment package version
  publish-test     Publish package to Test PyPI (test.pypi.org)
  publish-prod     Publish package to PyPI (pypi.org)
```

For prepare environment for development:

```bash
make env
```

Update project dependencies

```bash
make dependencies
```

Generate poetry.lock file

```bash
make lock
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

### License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.