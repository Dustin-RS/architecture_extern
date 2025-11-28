from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime
from typing import Protocol
import uuid

from money import Money

class IEvent: ...

@dataclass
class OrderPlacedEvent(IEvent):
    orderId: uuid.UUID
    userId: uuid.UUID
    amount: Money
    timestamp: datetime

class IEventHandler(Protocol):
    def handle(self, e: IEvent) -> None: ...

class EmailNotifier:
    def handle(self, e: IEvent) -> None:
        # send email (simulated)
        print(f"EmailNotifier: event received {e}")

class SellerNotifier:
    def handle(self, e: IEvent) -> None:
        print(f"SellerNotifier: event received {e}")

class AnalyticsHandler:
    def handle(self, e: IEvent) -> None:
        print(f"AnalyticsHandler: event received {e}")

class EventBus:
    def __init__(self):
        self._subscribers: dict[type, list[IEventHandler]] = defaultdict(list)

    def subscribe(self, typ: type, handler: IEventHandler) -> None:
        self._subscribers[typ].append(handler)

    def publish(self, e: IEvent) -> None:
        for handler in self._subscribers.get(type(e), []):
            handler.handle(e)

    def unsubscribe(self, typ: type, handler: IEventHandler) -> None:
        if handler in self._subscribers.get(typ, []):
            self._subscribers[typ].remove(handler)
