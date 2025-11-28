from dataclasses import dataclass
from decimal import Decimal
from enum import Enum
import uuid

from money import Money

@dataclass
class Item:
    listing_id: uuid.UUID
    quantity: int
    price_per_unit: Money

    def get_listing_id(self) -> uuid.UUID:
        return self.listing_id

    def get_quantity(self) -> int:
        return self.quantity

    def get_price_per_unit(self) -> Money:
        return self.price_per_unit

class OrderStatus(Enum):
    CREATED = "created"
    PAID = "paid"
    RESERVED = "reserved"
    SHIPPED = "shipped"
    CANCELLED = "cancelled"
    DELIVERED = "delivered"

class Order:
    def __init__(self, items: list[Item], buyer_id: uuid.UUID):
        self._id = uuid.uuid4()
        self._items = items
        self._buyer_id = buyer_id
        self._status = OrderStatus.CREATED
        self._total = self.calculate_total()

    def calculate_total(self) -> Money:
        total = Money(Decimal("0.0"), "USD")
        for it in self._items:
            total = total + (it.get_price_per_unit() * it.get_quantity())
        return total

    def get_id(self) -> uuid.UUID:
        return self._id

    def get_items(self) -> list[Item]:
        return list(self._items)

    def get_total(self) -> Money:
        return self._total

    def get_buyer_id(self) -> uuid.UUID:
        return self._buyer_id

    def get_status(self) -> OrderStatus:
        return self._status

    def set_status(self, s: OrderStatus) -> None:
        self._status = s