from dataclasses import dataclass
from datetime import datetime
from typing import Any
import uuid


@dataclass
class Listing:
    id: uuid.UUID
    product_type: str
    payload: dict[str, Any]
    created_at: datetime
    seller_id: uuid.UUID

    def get_id(self) -> uuid.UUID:
        return self.id

    def get_product_type(self) -> str:
        return self.product_type

    def get_payload(self) -> dict[str, Any]:
        return self.payload

    def get_created_at(self) -> datetime:
        return self.created_at

    def get_seller_id(self) -> uuid.UUID:
        return self.seller_id