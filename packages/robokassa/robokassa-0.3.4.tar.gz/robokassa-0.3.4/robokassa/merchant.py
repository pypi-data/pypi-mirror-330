from typing import Union

from robokassa.connection import Requests
from robokassa.utils import HttpResponseValidator


class BaseMerchant:
    pass


class Merchant(BaseMerchant):
    def __init__(self, http: Requests, merchant_login: str) -> None:
        self._http = http.connection

        self._merchant_login = merchant_login

    def get_currencies(self, language: str) -> dict:
        with self._http as conn:
            response = conn.post(
                url="WebService/Service.asmx/GetCurrencies",
                data={
                    "MerchantLogin": self._merchant_login,
                    "Language": language,
                },
            )
            validated_response = HttpResponseValidator(
                response, False
            ).validate_http_response()
            return validated_response

    def get_operation_state(
        self, signature_value: str, invoice_id: Union[int, str]
    ) -> dict:
        """
        Get state of operation.
        :param signature_value: MerchantLogin:InvoiceID:Password#2
        :param invoice_id: Store account number
        :return: dict
        """
        with self._http as conn:
            response = conn.post(
                url="WebService/Service.asmx/OpStateExt",
                data={
                    "MerchantLogin": self._merchant_login,
                    "InvoiceID": invoice_id,
                    "Signature": signature_value,
                },
            )
            validated_response = HttpResponseValidator(
                response, False
            ).validate_http_response()

            return validated_response
