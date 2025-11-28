from orders.models import Order
from orders.states import CreatedState, OrderState


class OrderContext:
    def __init__(self, order: Order):
        self.order = order
        self._state: OrderState = CreatedState()

    def set_state(self, s: OrderState) -> None:
        self._state = s

    def pay(self) -> None:
        self._state.pay(self)

    def cancel(self) -> None:
        self._state.cancel(self)

    def ship(self) -> None:
        self._state.ship(self)

    def deliver(self) -> None:
        self._state.deliver(self)

    def get_state(self) -> OrderState:
        return self._state

    def get_order(self) -> Order:
        return self.order