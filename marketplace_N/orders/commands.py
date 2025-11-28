from datetime import datetime
from typing import Optional, Protocol

from events.bus import OrderPlacedEvent
from orders.models import Order


class CommandResult:
    def __init__(self, success: bool, message: str = ""):
        self.success = success
        self.message = message

class ICommand(Protocol):
    def execute(self) -> CommandResult: ...
    def undo(self) -> None: ...

class PlaceOrderCommand:
    def __init__(self, order: Order,
                 event_bus: Optional[str]=None):
        self.order = order
        self._done = False
        self._event_bus = event_bus

    def execute(self) -> CommandResult:
        # in real life we would persist/order process
        self._done = True
        if self._event_bus:
            evt = OrderPlacedEvent(orderId=self.order.get_id(),
                                   userId=self.order.get_buyer_id(),
                                   amount=self.order.get_total(), timestamp=datetime.utcnow())
            self._event_bus.publish(evt)
        return CommandResult(True, "Order placed")

    def undo(self) -> None:
        if self._done:
            # revert placement
            self._done = False

class CapturePaymentCommand:
    def __init__(self, order: Order):
        self.order = order
        self._captured = False

    def execute(self) -> CommandResult:
        self._captured = True
        return CommandResult(True, "Payment captured")

    def undo(self) -> None:
        if self._captured:
            self._captured = False

class CommandBus:
    def __init__(self):
        self._queue: list[ICommand] = []
        self._history: list[ICommand] = []

    def enqueue(self, cmd: ICommand) -> None:
        self._queue.append(cmd)

    def execute_next(self) -> CommandResult:
        if not self._queue:
            return CommandResult(False, "Empty queue")
        cmd = self._queue.pop(0)
        res = cmd.execute()
        if res.success:
            self._history.append(cmd)
        return res

    def undo_last(self) -> None:
        if not self._history:
            return
        cmd = self._history.pop()
        cmd.undo()

    def get_queue(self) -> list[ICommand]:
        return list(self._queue)

