from dataclasses import dataclass
from typing import Any
import uuid

from money import Money

@dataclass
class ListingDTO:
    title: str
    price: Money
    category_code: str
    attributes: dict[str, Any]
    seller_id: uuid.UUID