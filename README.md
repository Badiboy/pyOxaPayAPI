[![PyPi Package Version](https://img.shields.io/pypi/v/pyOxaPayAPI.svg)](https://pypi.python.org/pypi/pyOxaPayAPI)
[![Supported Python versions](https://img.shields.io/pypi/pyversions/pyOxaPayAPI.svg)](https://pypi.python.org/pypi/pyOxaPayAPI)
[![PyPi downloads](https://img.shields.io/pypi/dm/pyOxaPayAPI.svg)](https://pypi.org/project/pyOxaPayAPI/)

# <p align="center">pyOxaPayAPI</p>
Python implementation of [OxaPay](https://oxapay.com) pubilc [API](https://docs.oxapay.com)

_**This library is based on [oxapay_api](https://github.com/Rushifakami/oxapay_api) implementation. Was forked here due to slow PR acceptance.**_

**This library is ACTUAL and is supported. If you need some not implemented methods - just open an issue.**

# Installation
Installation using pip (a Python package manager):
```
$ pip install pyOxaPayAPI
```

# Usage
Everything is as simple as the [API](https://docs.oxapay.com/) itself.
1. Create pyOxaPayAPI instance
2. Access API methods in pythonic notation (e.g. "Creating an invoice" -> create_invoice())
3. Most methods return result as correspondent class, so you can access data as fields 
```
from pyOxaPayAPI import pyOxaPayAPI
client = pyOxaPayAPI(
    "xxxxxxx",                   # Merchand API key
    general_api_key="xxxxxxx",   # General API key (for account methods like "balance")
    payout_api_key="xxxxxxx")    # Payout API key (for payout methods)
balances = client.get_account_balance(currency=currency.name)
for currency, balance in balances["data"].items():
    print("Merchant balance: {} {}".format(balance, currency))
```
You can also check tests.py.

# Exceptions
Exceptions are rised using pyOxaPayAPIException class.
