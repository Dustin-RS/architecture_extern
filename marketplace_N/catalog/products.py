from abc import ABC, abstractmethod
from typing import Any, Optional
import uuid

from money import Money

class ValidationError(Exception):
    pass

class AbstractProduct(ABC):
    def __init__(self, title: str, price: Money, attributes: dict[str, Any], id: Optional[uuid.UUID]=None):
        self._id = id or uuid.uuid4()
        self._title = title
        self._price = price
        self._attributes = attributes or {}

    def validate(self) -> None:
        # default: no-op, subclasses or factory validators can enforce rules
        pass

    def get_id(self) -> uuid.UUID:
        return self._id

    def get_title(self) -> str:
        return self._title

    def get_price(self) -> Money:
        return self._price

    def get_attributes(self) -> dict[str, Any]:
        return self._attributes

class ElectronicProduct(AbstractProduct):
    def __init__(self, title: str, price: Money, attributes: dict[str, Any]):
        super().__init__(title, price, attributes)
        self.warranty_months = int(attributes.get("warranty_months", 0))
        self.brand = attributes.get("brand")
        self.model = attributes.get("model")

    def get_warranty_months(self) -> int:
        return self.warranty_months

    def get_brand(self) -> Optional[str]:
        return self.brand

    def get_model(self) -> Optional[str]:
        return self.model

class ClothingProduct(AbstractProduct):
    def __init__(self, title: str, price: Money, attributes: dict[str, Any]):
        super().__init__(title, price, attributes)
        self.size = attributes.get("size")
        self.material = attributes.get("material")
        self.gender = attributes.get("gender")

    def get_size(self) -> Optional[str]:
        return self.size

    def get_material(self) -> Optional[str]:
        return self.material

    def get_gender(self) -> Optional[str]:
        return self.gender

class BookProduct(AbstractProduct):
    def __init__(self, title: str, price: Money, attributes: dict[str, Any]):
        super().__init__(title, price, attributes)
        self.author = attributes.get("author")
        self.genre = attributes.get("genre")
        self.publication_year = attributes.get("publication_year")

    def get_author(self) -> Optional[str]:
        return self.author

    def get_genre(self) -> Optional[str]:
        return self.genre

    def get_publication_year(self) -> Optional[int]:
        return self.publication_year
