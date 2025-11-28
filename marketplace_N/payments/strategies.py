from typing import Any, Optional, Protocol

from orders.models import Order
from payments.gateways import IPaymentGateway


class PaymentResult:
    def __init__(self, success: bool, tx_id: Optional[str] = None, message: str = ""):
        self.success = success
        self.tx_id = tx_id
        self.message = message

class IPaymentStrategy(Protocol):
    def execute_payment(self, order: Order, payment_data: dict[str, Any]) -> PaymentResult: ...

class StripeStrategy:
    def __init__(self, gateway: IPaymentGateway):
        self.gateway = gateway

    def execute_payment(self, order: Order, payment_data: dict[str, Any]) -> PaymentResult:
        resp = self.gateway.authorize(order.get_total(), payment_data)
        return PaymentResult(resp.success, resp.tx_id, resp.message)

class PayPalStrategy:
    def __init__(self, gateway: IPaymentGateway):
        self.gateway = gateway

    def execute_payment(self, order: Order, payment_data: dict[str, Any]) -> PaymentResult:
        resp = self.gateway.authorize(order.get_total(), payment_data)
        return PaymentResult(resp.success, resp.tx_id, resp.message)

class BankStrategy:
    def __init__(self, gateway: IPaymentGateway):
        self.gateway = gateway

    def execute_payment(self, order: Order, payment_data: dict[str, Any]) -> PaymentResult:
        resp = self.gateway.authorize(order.get_total(), payment_data)
        return PaymentResult(resp.success, resp.tx_id, resp.message)