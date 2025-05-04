import requests
from typing import Optional

API_URL = "https://api.oxapay.com/v1"


# noinspection PyPep8Naming
class pyOxaPayAPIException(Exception):
    def __init__(self, message, full_error = ""):
        self.message = message
        self.full_error = full_error
        super().__init__(self.message)


# noinspection PyPep8Naming
class pyOxaPayAPI:
    """
    OxaPay API Client
    """

    def __init__(
            self,
            merchant_api_key: str,
            general_api_key: Optional[str] = None,
            payout_api_key: Optional[str] = None,
            print_errors: Optional[bool] = False,
            timeout: Optional[int] = None
    ):
        """
        Create the pyOxaPayAPI instance.

        :param merchant_api_key: The merchant's API key for authentication for payments processing
        :param general_api_key: (Optional) general API key for authentication for account requests
        :param payout_api_key: (Optional) payout API key for authentication for payouts processing
        :param print_errors: (Optional) Print dumps on request errors
        :param timeout: (Optional) Timeout for requests in seconds
        """
        self.print_errors = print_errors
        self.timeout = timeout
        self.headers = {
            "merchant_api_key": merchant_api_key,
            "Content-Type": "application/json"
        }
        if general_api_key:
            self.headers["general_api_key"] = general_api_key
        if payout_api_key:
            self.headers["payout_api_key"] = payout_api_key

    def __request(self, method: str, endpoint: str, query_params=None, json_data=None):
        url = f'{API_URL}/{endpoint}'

        if (method == 'GET') and query_params:
            response = requests.request(headers=self.headers, method=method, url=url, params=query_params, timeout=self.timeout)
        else:
            response = requests.request(headers=self.headers, method=method, url=url, json=json_data, timeout=self.timeout)

        if response.status_code == 200:
            if response.headers.get('content-type') == 'application/json':
                return response.json()
            else:
                return response.text
        elif response.status_code == 400:
            raise ValueError(response.json())
        else:
            raise pyOxaPayAPIException(f'Failed to make request: {response.status_code} - {response.reason}')
        #     base_resp = requests.post(self.api_url + method_url, data=pre_sign, headers=headers, timeout=self.timeout)
        #     resp = base_resp.json()
        # except ValueError as ve:
        #     code = base_resp.status_code if base_resp else -2
        #     message = "Response decode failed: {}".format(ve)
        #     if self.print_errors:
        #         print(message)
        #     raise pyOxaPayAPIException(code, message)
        # except pyOxaPayAPIException as pe:
        #     raise pe
        # except pyOxaPayAPIException as e:
        #     code = base_resp.status_code if base_resp else -3
        #     message = "Request unknown exception: {}".format(e)
        #     if self.print_errors:
        #         print(message)
        #     raise pyOxaPayAPIException(code, message)
        # if not resp:
        #     code = base_resp.status_code if base_resp else -4
        #     message = "None request response"
        #     if self.print_errors:
        #         print(message)
        #     raise pyOxaPayAPIException(code, message)
        # elif not resp.get("result"):
        #     code = base_resp.status_code if base_resp else -5
        #     if resp.get("message"):
        #         message = resp["message"]
        #     elif resp.get("errors"):
        #         message = resp["errors"]
        #     else:
        #         message = "No error info provided"
        #     if self.print_errors:
        #         print("Response: {}".format(resp))
        #     raise pyOxaPayAPIException(code, message)
        # # code -6 is used above
        # else:
        #     return resp

    def system_status(self):
        """
        Check the current status of the OxaPay API, ensuring it is functioning correctly
        :return: The API status information
        """
        try:
            return self.__request('GET', 'common/monitor')
        except Exception as e:
            raise pyOxaPayAPIException(f"Error getting status: {e}")

    def generate_invoice(
            self,
            amount: float,
            currency: str = None,
            lifetime: int = 60,
            fee_paid_by_payer: float = None,
            under_paid_coverage: float = None,
            to_currency: str = None,
            auto_withdrawal: bool = False,
            mixed_payment: bool = None,
            callback_url: str = None,
            return_url: str = None,
            email: str = None,
            order_id: str = None,
            thanks_message: str = None,
            description: str = None,
            sandbox: bool = False,
    ):
        """
        Generate a new invoice and obtain a payment URL for completing the transaction. By providing the required parameters in your request, you can specify the invoice amount and customize various options for the payment process.

        :param amount: The amount for the payment. If the currency field is not filled, the amount should be specified in dollars. If the currency field is filled, the amount should correspond to the specified currency.
        :param currency: Specify the currency symbol if you want the invoice amount calculated with a specific currency. You can also create invoices in fiat currencies.
        :param lifetime: Set the expiration time for the payment link in minutes (15-2880). Default: 60.
        :param fee_paid_by_payer: Specify whether the payer will cover the invoice commission. 1 indicates that the payer will pay the fee, while 0 indicates that the merchant will pay the fee. Default: Merchant setting.
        :param under_paid_coverage: Specify the acceptable inaccuracy in payment. Determines the maximum acceptable difference between the requested and paid amount (0-60.00). Default: Merchant setting.
        :param to_currency: The currency symbol of the cryptocurrency you want to convert to. You only can convert paid crypto currencies to USDT.
        :param auto_withdrawal: 1 indicates that the received currency will be sent to the address specified in your Address List on the Settings page and 0 indicates that the amount will be credited to your OxaPay balance.
        :param mixed_payment: Specify whether the payer can cover the remaining amount with another currency if they pay less than the invoice amount. 1 allows the user to pay the remainder with a different coin, while 0 doesn't allow it. Default: Merchant setting.
        :param callback_url: The URL where payment information will be sent. Use this to receive notifications about the payment status.
        :param return_url: The URL where the payer will be redirected after a successful payment.
        :param email: Provide the payer's email address for reporting purposes.
        :param order_id: Specify a unique order ID for reference in your system.
        :param thanks_message: A thanks message that brief note displayed to the payer after a successful payment.
        :param description: Provide order details or any additional information that will be shown in different reports.
        :param sandbox: The sandbox field is a boolean that specifies whether the API request should operate in sandbox mode (test environment). Set it to true for testing and false for live transactions.
        :return: The result of the invoice creation process, either as a raw response or as an OrderStatus object.
        """
        params = {
            'amount': amount,
            'currency': currency,
            'lifetime': lifetime,
            'fee_paid_by_payer': fee_paid_by_payer,
            'under_paid_coverage': under_paid_coverage,
            'to_currency': to_currency,
            'auto_withdrawal': auto_withdrawal,
            'mixed_payment': mixed_payment,
            'callback_url': callback_url,
            'return_url': return_url,
            'email': email,
            'order_id': order_id,
            'thanks_message': thanks_message,
            'description': description,
            'sandbox': sandbox,
        }
        query_params = {k: v for k, v in params.items() if v is not None}
        try:
            response_data = self.__request('POST', 'payment/invoice', json_data=query_params)
            return response_data
        except Exception as e:
            raise pyOxaPayAPIException(f"Error creating invoice: {e}")

    def supported_currencies(self):
        """
        Retrieves a list of supported currencies and their network details.

        :return: A list of supported currencies with their details.
        """
        try:
            return self.__request('GET', 'common/currencies')
        except Exception as e:
            raise pyOxaPayAPIException(f"Error getting supported currencies: {e}")

    def supported_networks(self):
        """
        Retrieves a list of supported blockchain networks for cryptocurrency transactions.

        :return: A list of supported blockchain networks.
        """
        try:
            return self.__request('GET', 'common/networks')
        except Exception as e:
            raise pyOxaPayAPIException(f"Error getting supported networks: {e}")

    def supported_fiat_currencies(self):
        """
        Retrieves a list of supported fiat currencies and their details.

        :return: A list of supported fiat currencies with their details.
        """
        try:
            return self.__request('GET', 'common/fiats')
        except Exception as e:
            raise pyOxaPayAPIException (f"Error getting supported fiat currencies: {e}")

    def payment_information(self, track_id: int):
        """
        Retrieve detailed information about a specific payment using its track_id. After generating an invoice, you will receive a track_id, which serves as a reference for requesting payment details.

        :param track_id: The unique identifier for the payment transaction.
        :return: The payment information, either as a raw response or as a PaymentStatus object.
        """
        try:
            response_data = self.__request('GET', f'payment/{track_id}')
            return response_data
        except Exception as e:
            raise pyOxaPayAPIException(f"Error getting payment information: {e}")

    def generate_white_label(
            self,
            pay_currency: str,
            amount: float,
            currency: str = None,
            network: str = None,
            lifetime: int = 60,
            fee_paid_by_payer: float = None,
            under_paid_coverage: float = None,
            to_currency: str = None,
            auto_withdrawal: bool = False,
            callback_url: str = None,
            email: str = None,
            order_id: str = None,
            description: str = None
    ):
        """
        Generate white-labeled payment solutions, delivering a fully branded payment experience powered by the OxaPay gateway. Instead of generating an invoice URL, this endpoint provides comprehensive payment details, including the payment address, currency, amount, expiration time, and other relevant information, enabling you to manage the payment process within your own interface.

        :param pay_currency: Specify the currency symbol if you want the invoice to be paid in a specific currency. Defines the currency in which you wish to receive your settlements.
        :param amount: The amount for the payment. If the currency field is not filled, the amount should be specified in dollars. If the currency field is filled, the amount should correspond to the specified currency.
        :param currency: Specify the currency symbol if you want the invoice amount calculated with a specific currency. You can also create invoices in fiat currencies.
        :param network: The blockchain network on which the payment should be created. If not specified, the default network will be used.
        :param lifetime: Set the expiration time for the payment link in minutes (15-2880). Default: 60.
        :param fee_paid_by_payer: Specify whether the payer will cover the invoice commission. 1 indicates that the payer will pay the fee, while 0 indicates that the merchant will pay the fee. Default: Merchant setting.
        :param under_paid_coverage: Specify the acceptable inaccuracy in payment. Determines the maximum acceptable difference between the requested and paid amount (0-60.00). Default: Merchant setting.
        :param to_currency: The currency symbol of the cryptocurrency you want to convert to. You only can convert paid crypto currencies to USDT.
        :param auto_withdrawal: 1 indicates that the received currency will be sent to the address specified in your Address List on the Settings page and 0 indicates that the amount will be credited to your OxaPay balance.
        :param callback_url: The URL where payment information will be sent. Use this to receive notifications about the payment status.
        :param email: Provide the payer's email address for reporting purposes.
        :param order_id: Specify a unique order ID for reference in your system.
        :param description: Provide order details or any additional information that will be shown in different reports.
        :return: The result of the white label payment creation process.
        """
        params = {
            'pay_currency': pay_currency,
            'amount': amount,
            'currency': currency,
            'network': network,
            'lifetime': lifetime,
            'fee_paid_by_payer': fee_paid_by_payer,
            'under_paid_coverage': under_paid_coverage,
            'to_currency': to_currency,
            'auto_withdrawal': auto_withdrawal,
            'callback_url': callback_url,
            'email': email,
            'order_id': order_id,
            'description': description,
        }
        query_params = {k: v for k, v in params.items() if v is not None}
        try:
            return self.__request('POST', 'payment/white-label', json_data=query_params)
        except Exception as e:
            raise pyOxaPayAPIException(f"Error creating white label payment: {e}")

    def generate_static_address(
            self,
            network: str,
            to_currency: str = None,
            auto_withdrawal: bool = False,
            callback_url: str = None,
            email: str = None,
            order_id: str = None,
            description: str = None,
    ):
        """
        Generate a static address for a specific currency and network. The static address will be linked to a unique track_id, and if a callback_url is provided, your server will receive notifications for any payments made to the address. This enables you to track and receive transactions to the static address, regardless of the amount or timing.

        :param network: The blockchain network on which the static address should be created.
        :param to_currency: The currency symbol of the cryptocurrency you want to convert to.
        :param auto_withdrawal: 1 indicates that the received currency will be sent to the address specified in your Address List on the Settings page and 0 indicates that the amount will be credited to your OxaPay balance.
        :param callback_url: The URL where payment information will be sent. Use this to receive notifications about payments made to the static address.
        :param email: Provide the payer's email address for reporting purposes.
        :param order_id: Specify a unique order ID for reference in your system.
        :param description: Provide order details or any additional information that will be shown in different reports.
        :return: The result of the static address creation process.
        """
        params = {
            'network': network,
            'to_currency': to_currency,
            'auto_withdrawal': auto_withdrawal,
            'callback_url': callback_url,
            'email': email,
            'order_id': order_id,
            'description': description,
        }
        query_params = {k: v for k, v in params.items() if v is not None}
        try:
            return self.__request('POST', 'payment/static-address', json_data=query_params)
        except Exception as e:
            raise pyOxaPayAPIException(f"Error creating static address: {e}")

    def revoke_static_address(self, address: str):
        """
        Revokes a static wallet by disabling further transactions to the specified address.

        :param address: The address of the static wallet to revoke.
        :return: The result of the revocation process.
        """
        params = {
            'address': address
        }
        try:
            return self.__request('POST', 'payment/static-address/revoke', json_data=params)
        except Exception as e:
            raise pyOxaPayAPIException(f"Error revoking static wallet: {e}")

    def static_address_list(
            self,
            track_id: int = None,
            network: str = None,
            currency: str = None,
            address: str = None,
            have_tx: bool = None,
            order_id: str = None,
            email: str = None,
            page: int = 1,
            size: int = 10,
    ):
        """
        Use this endpoint to retrieve a list of static addresses associated with a specific business. The list can be filtered by various criteria, such as trackId, address, network, email and orderId. Pagination is also available to fetch the results in smaller sets.

        :param track_id: Filter addresses by a specific ID. Defaults to None.
        :param network: Filter addresses by the expected blockchain network for the specified crypto currency. Defaults to None.
        :param currency: Filter addresses by the expected currency. Defaults to None.
        :param address: Filter static addresses by the expected address. It’s better to filter static addresses. Defaults to None.
        :param have_tx: Filter the addresses that had transactions. Defaults to None.
        :param order_id: Filter addresses by a unique order ID for reference. Defaults to None.
        :param email: Filter addresses by the email. Defaults to None.
        :param page: The page number of the results you want to retrieve. Possible values: from 1 to the total number of pages - default 1.
        :param size: Number of records to display per page. Possible values: from 1 to 200. Default: 1.
        :return:
        """
        params = {
            'track_id': track_id,
            'network': network,
            'currency': currency,
            'address': address,
            'have_tx': have_tx,
            'order_id': order_id,
            'email': email,
            'page': page,
            'size': size,
        }
        query_params = {k: v for k, v in params.items() if v is not None}
        try:
            return self.__request('GET', 'payment/static-address', query_params=query_params)
        except Exception as e:
            raise pyOxaPayAPIException(f"Error getting static address list: {e}")

    # noinspection PyShadowingBuiltins
    def payment_history(
            self,
            track_id: int = None,
            type: str = None,
            status: str = None,
            pay_currency: str = None,
            currency: str = None,
            network: str = None,
            address: str = None,
            from_date: int = None,
            to_date: int = None,
            from_amount: float = None,
            to_amount: float = None,
            sort_by: str = 'create_date',
            sort_type: str = 'desc',
            page: int = 1,
            size: int = 10,
    ):
        """
        Retrieves the payment history based on specified filters.

        :param track_id: Filter payments by a specific invoice ID. Defaults to None.
        :param type: Filter payments by type (e.g., 'Invoice', 'White-Label', 'Static Wallet'). Defaults to None.
        :param status: Filter payments by status (e.g., 'Paid', 'Confirming'). Defaults to None.
        :param pay_currency: Filter payments by a specific crypto currency symbol in which the pay amount is specified. Defaults to None.
        :param currency: Filter payments by a specific currency symbol. Defaults to None.
        :param network: Filter payments by the expected blockchain network for the specified crypto currency. Defaults to None.
        :param address: Filter payments by the expected address. It’s better to filter static addresses. Defaults to None.
        :param from_date: The start of the date window to query for payments in Unix format. Defaults to None.
        :param to_date: The end of the date window to query for payments in Unix format. Defaults to None.
        :param from_amount: Filter payments with amounts greater than or equal to the specified value. Defaults to None.
        :param to_amount: Filter payments with amounts less than or equal to the specified value. Defaults to None.
        :param sort_by: Sort the received list by a parameter. Possible values: 'create_date', 'pay_date', 'amount'. Default: 'create_date'.
        :param sort_type: Display the list in ascending or descending order. Possible values: 'asc', 'desc'. Default: 'desc'.
        :param page: The page number of the results to retrieve. Possible values: from 1 to the total number of pages. Default: 1.
        :param size: Number of records to display per page. Possible values: from 1 to 200. Default: 10.
        :return: The payment history.
        """
        params = {
            'track_id': track_id,
            'type': type,
            'status': status,
            'pay_currency': pay_currency,
            'currency': currency,
            'network': network,
            'address': address,
            'from_date': from_date,
            'to_date': to_date,
            'from_amount': from_amount,
            'to_amount': to_amount,
            'sort_by': sort_by,
            'sort_type': sort_type,
            'page': page,
            'size': size,
        }
        query_params = {k: v for k, v in params.items() if v is not None}
        try:
            return self.__request('GET', 'payment', query_params=query_params)
        except Exception as e:
            raise pyOxaPayAPIException(f"Error getting payment history: {e}")

    def accepted_currencies(self):
        """
        retrieves the list of cryptocurrencies available for payment processing through OxaPay. These currencies are configured by you on the "Merchant Service" page of your account, specifying the cryptocurrencies your business accepts for payments.

        :return: The list of accepted cryptocurrencies for payment processing.
        """
        try:
            return self.__request('GET', 'payment/accepted-currencies')
        except Exception as e:
            raise pyOxaPayAPIException(f"Error getting accepted currencies: {e}")

    def prices(self):
        """
        Retrieves the current prices of all cryptocurrencies supported by OxaPay.

        :return: The current prices of all supported cryptocurrencies.
        """
        try:
            return self.__request('GET', 'common/prices')
        except Exception as e:
            raise pyOxaPayAPIException(f"Error getting prices: {e}")

    def account_balance(self, currency: str = None):
        """
        Retrieves the account balance for all wallets associated with a user.

        :param currency: Optional. Specify a specific currency to get the balance for that currency.
        :return: The account balance information.
        """
        params = {
            'currency': currency
        }
        query_params = {k: v for k, v in params.items() if v is not None}
        try:
            return self.__request('GET', 'general/account/balance', query_params=query_params)
        except Exception as e:
            raise pyOxaPayAPIException(f"Error getting account balance: {e}")

    def generate_payout(
            self,
            address: str,
            currency: str,
            amount: float,
            network: str = None,
            callback_url: str = None,
            memo: str = None,
            description: str = None,
    ):
        """
        Generates a cryptocurrency payout request.

        :param address: The recipient's cryptocurrency address where the payout will be sent.
        :param currency: The symbol of the cryptocurrency to be sent (e.g., BTC, ETH, LTC, etc.).
        :param amount: The exact amount of cryptocurrency to be sent as the payout.
        :param network: The blockchain network to be used for the payout. Required for currencies with multi supported networks.
        :param callback_url: The URL for sending payment status updates.
        :param memo: A memo or tag for transactions on supported networks (e.g., for TON).
        :param description: A description or additional information for the payout, useful for reports.
        :return: The result of the payout generation process.
        """
        params = {
            'address': address,
            'currency': currency,
            'amount': amount,
            'network': network,
            'callback_url': callback_url,
            'memo': memo,
            'description': description,
        }
        query_params = {k: v for k, v in params.items() if v is not None}
        try:
            return self.__request('POST', 'payout', json_data=query_params)
        except Exception as e:
            raise pyOxaPayAPIException(f"Error creating payout: {e}")

    def payout_information(self, track_id: int):
        """
        Retrieve detailed information about a specific payout using its track_id. After generating a payout request, you will receive a track_id, which serves as a reference for requesting payout details.

        :param track_id: The unique identifier for the payout transaction.
        :return: The payout information, either as a raw response or as a PayoutStatus object.
        """
        try:
            return self.__request('GET', f'payout/{track_id}')
        except Exception as e:
            raise pyOxaPayAPIException(f"Error getting payout information: {e}")

    # noinspection PyShadowingBuiltins
    def payout_history(
            self,
            status: str = None,
            type: str = None,
            currency: str = None,
            network: str = None,
            from_amount: float = None,
            to_amount: float = None,
            from_date: int = None,
            to_date: int = None,
            sort_by: str = 'create_date',
            sort_type: str = 'desc',
            page: int = 1,
            size: int = 10
    ):
        """
        Retrieves the payout history based on specified filters.

        :param status: Filter payouts based on their status (processing, complete, rejected, etc.). Defaults to None.
        :param type: Filter payouts based on type (internal or external). Defaults to None.
        :param currency: Specify the currency symbol for filtering payouts in a specific currency. Defaults to None.
        :param network: Specify the blockchain network for filtering payouts on a particular network. Defaults to None.
        :param from_amount: Specify the minimum payout amount for filtering. Defaults to None.
        :param to_amount: Specify the maximum payout amount for filtering. Defaults to None.
        :param from_date: The start of the date window to query for payouts in Unix format. Defaults to None.
        :param to_date: The end of the date window to query for payouts in Unix format. Defaults to None.
        :param sort_by: Sort the received list by a parameter. Possible values: 'create_date', 'pay_date', 'amount'. Default: 'create_date'.
        :param sort_type: Display the list in ascending or descending order. Possible values: 'asc', 'desc'. Default: 'desc'.
        :param page: The page number of the results you want to retrieve. Possible values: from 1 to the total number of pages. Default: 1.
        :param size: Number of records to display per page. Possible values: from 1 to 200. Default: 10.
        :return:
        """
        params = {
            'status': status,
            'type': type,
            'currency': currency,
            'network': network,
            'from_amount': from_amount,
            'to_amount': to_amount,
            'from_date': from_date,
            'to_date': to_date,
            'sort_by': sort_by,
            'sort_type': sort_type,
            'page': page,
            'size': size,
        }
        query_params = {k: v for k, v in params.items() if v is not None}
        try:
            return self.__request('GET', 'payout', query_params=query_params)
        except Exception as e:
            raise pyOxaPayAPIException(f"Error getting payout history: {e}")
