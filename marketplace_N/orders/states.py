from abc import ABC, abstractmethod
from typing import Any
from orders.models import OrderStatus
    

class OrderState(ABC):
    def __init__(self, name: str):
        self._name = name

    def get_name(self) -> str:
        return self._name

    @abstractmethod
    def pay(self, context: Any) -> None: ...

    @abstractmethod
    def cancel(self, context: Any) -> None: ...

    @abstractmethod
    def ship(self, context: Any) -> None: ...

    @abstractmethod
    def deliver(self, context: Any) -> None: ...

class CreatedState(OrderState):
    def __init__(self):
        super().__init__("created")

    def pay(self, context: Any) -> None:
        context.order.set_status(OrderStatus.PAID)
        context.set_state(PaidState())

    def cancel(self, context: Any) -> None:
        context.order.set_status(OrderStatus.CANCELLED)
        context.set_state(CancelledState())

    def ship(self, context: Any) -> None:
        raise Exception("Can't ship before payment")

    def deliver(self, context: Any) -> None:
        raise Exception("Can't deliver before shipping")

class PaidState(OrderState):
    def __init__(self):
        super().__init__("paid")

    def pay(self, context: Any) -> None:
        pass

    def cancel(self, context: Any) -> None:
        context.order.set_status(OrderStatus.CANCELLED)
        context.set_state(CancelledState())

    def ship(self, context: Any) -> None:
        context.order.set_status(OrderStatus.SHIPPED)
        context.set_state(ShippedState())

    def deliver(self, context: Any) -> None:
        raise Exception("Can't deliver before shipping")

class ReservedState(OrderState):
    def __init__(self):
        super().__init__("reserved")

    def pay(self, context: Any) -> None:
        context.order.set_status(OrderStatus.PAID)
        context.set_state(PaidState())

    def cancel(self, context: Any) -> None:
        context.order.set_status(OrderStatus.CANCELLED)
        context.set_state(CancelledState())

    def ship(self, context: Any) -> None:
        context.order.set_status(OrderStatus.SHIPPED)
        context.set_state(ShippedState())

    def deliver(self, context: Any) -> None:
        raise Exception("Can't deliver before shipping")

class ShippedState(OrderState):
    def __init__(self):
        super().__init__("shipped")

    def pay(self, context: Any) -> None:
        pass

    def cancel(self, context: Any) -> None:
        raise Exception("Can't cancel after shipped")

    def ship(self, context: Any) -> None:
        pass

    def deliver(self, context: Any) -> None:
        context.order.set_status(OrderStatus.DELIVERED)
        context.set_state(self)

class CancelledState(OrderState):
    def __init__(self):
        super().__init__("cancelled")

    def pay(self, context: Any) -> None:
        raise Exception("Can't pay cancelled order")

    def cancel(self, context: Any) -> None:
        pass

    def ship(self, context: Any) -> None:
        raise Exception("Can't ship cancelled order")

    def deliver(self, context: Any) -> None:
        raise Exception("Can't deliver cancelled order")