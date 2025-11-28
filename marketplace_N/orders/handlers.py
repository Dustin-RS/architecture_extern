from abc import ABC, abstractmethod
from typing import Optional
from orders.context import OrderContext


class OrderHandler(ABC):
    def __init__(self):
        self._next: Optional["OrderHandler"] = None

    def set_next(self, h: "OrderHandler") -> "OrderHandler":
        self._next = h
        return h

    @abstractmethod
    def handle(self, ctx: OrderContext) -> bool: ...

class CartValidationHandler(OrderHandler):
    def handle(self, ctx: OrderContext) -> bool:
        if not ctx.order.get_items():
            return False
        if self._next:
            return self._next.handle(ctx)
        return True

class StockReservationHandler(OrderHandler):
    def handle(self, ctx: OrderContext) -> bool:
        # assume stock ok
        if self._next:
            return self._next.handle(ctx)
        return True

class PaymentValidationHandler(OrderHandler):
    def handle(self, ctx: OrderContext) -> bool:
        # assume payment validated
        if self._next:
            return self._next.handle(ctx)
        return True

class FraudCheckHandler(OrderHandler):
    def handle(self, ctx: OrderContext) -> bool:
        # assume no fraud
        if self._next:
            return self._next.handle(ctx)
        return True
