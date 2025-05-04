try:
    from pyOxaPayAPI import pyOxaPayAPI, pyOxaPayAPIException
except:
    from api import pyOxaPayAPI, pyOxaPayAPIException

try:
    from private_keys import *
except:
    test_merchant_api_key = None
    test_general_api_key = None

def test_api_functions():
    client = pyOxaPayAPI(
        test_merchant_api_key,
        general_api_key=test_general_api_key,
        print_errors=True)
    print("API status: ", client.system_status()["data"])
    print("Supported currencies: ", client.supported_currencies()["data"])
    print("Supported networks: ", client.supported_networks()["data"])
    print("Supported fiat currencies: ", client.supported_fiat_currencies()["data"])
    print("Get prices: ", client.get_prices()["data"])

    if test_merchant_api_key:
        invoice = client.generate_invoice(1, "USDT")["data"]
        print("Create invoice: ", invoice)
        track_id = invoice["track_id"]
        print("Payment information: ", client.payment_information(track_id)["data"])
        address = client.generate_static_address("TRON")["data"]
        print("Create static address: ", address)
        track_id = address["track_id"]
        address = address["address"]
        print("Get static address list: ", client.static_address_list(track_id=track_id)["data"])
        print("Revoke static wallet: ", client.revoke_static_address(address)["data"])
        print("Get payment history: ", client.payment_history()["data"]["list"])
        print("Get accepted currencies: ", client.accepted_currencies()["data"])

    if test_general_api_key:
        print("Balances: ", client.account_balance()["data"])
        print("Balance TRX: ", client.account_balance("TRX")["data"])

test_api_functions()
