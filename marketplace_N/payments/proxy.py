from typing import Any, Optional
from money import Money
from payments.gateways import IPaymentGateway, PaymentResponse


class RetryPolicy:
    def __init__(self, attempts: int = 3):
        self.attempts = attempts

class PaymentGatewayProxy(IPaymentGateway):
    def __init__(self, inner: IPaymentGateway, retry_policy: RetryPolicy):
        self.inner = inner
        self.retry_policy = retry_policy

    def authorize(self, amount: Money, data: dict[str, Any]) -> PaymentResponse:
        last: Optional[PaymentResponse] = None
        for _ in range(self.retry_policy.attempts):
            last = self.inner.authorize(amount, data)
            if last.success:
                return last
        return last or PaymentResponse(False, None, "failed")

    def capture(self, tx_id: str) -> PaymentResponse:
        last: Optional[PaymentResponse] = None
        for _ in range(self.retry_policy.attempts):
            last = self.inner.capture(tx_id)
            if last.success:
                return last
        return last or PaymentResponse(False, None, "failed")

    def refund(self, tx_id: str) -> PaymentResponse:
        last: Optional[PaymentResponse] = None
        for _ in range(self.retry_policy.attempts):
            last = self.inner.refund(tx_id)
            if last.success:
                return last
        return last or PaymentResponse(False, None, "failed")
