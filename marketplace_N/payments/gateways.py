from typing import Any, Optional, Protocol
import uuid

from money import Money


class PaymentResponse:
    def __init__(self, success: bool, tx_id: Optional[str] = None, message: str = ""):
        self.success = success
        self.tx_id = tx_id
        self.message = message

class IPaymentGateway(Protocol):
    def authorize(self, amount: Money, data: dict[str, Any]) -> PaymentResponse: ...
    def capture(self, tx_id: str) -> PaymentResponse: ...
    def refund(self, tx_id: str) -> PaymentResponse: ...

class StripeAdapter:
    def __init__(self, api_key: str):
        self.api_key = api_key

    def authorize(self, amount: Money, data: dict[str, Any]) -> PaymentResponse:
        return PaymentResponse(True, tx_id=str(uuid.uuid4()), message="stripe authorized")

    def capture(self, tx_id: str) -> PaymentResponse:
        return PaymentResponse(True, tx_id=tx_id, message="stripe captured")

    def refund(self, tx_id: str) -> PaymentResponse:
        return PaymentResponse(True, tx_id=tx_id, message="stripe refunded")

class PayPalAdapter:
    def __init__(self, client_id: str, client_secret: str):
        self.client_id = client_id
        self.client_secret = client_secret

    def authorize(self, amount: Money, data: dict[str, Any]) -> PaymentResponse:
        return PaymentResponse(True, tx_id=str(uuid.uuid4()), message="paypal authorized")

    def capture(self, tx_id: str) -> PaymentResponse:
        return PaymentResponse(True, tx_id=tx_id, message="paypal captured")

    def refund(self, tx_id: str) -> PaymentResponse:
        return PaymentResponse(True, tx_id=tx_id, message="paypal refunded")

class BankAdapter:
    def __init__(self, endpoint: str):
        self.endpoint = endpoint

    def authorize(self, amount: Money, data: dict[str, Any]) -> PaymentResponse:
        return PaymentResponse(True, tx_id=str(uuid.uuid4()), message="bank authorized")

    def capture(self, tx_id: str) -> PaymentResponse:
        return PaymentResponse(True, tx_id=tx_id, message="bank captured")

    def refund(self, tx_id: str) -> PaymentResponse:
        return PaymentResponse(True, tx_id=tx_id, message="bank refunded")
