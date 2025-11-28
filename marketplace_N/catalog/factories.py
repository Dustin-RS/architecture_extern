from __future__ import annotations
from dataclasses import dataclass, field
from decimal import Decimal
from typing import Any, Optional, Protocol, runtime_checkable, Callable
from abc import ABC, abstractmethod
import uuid
from datetime import datetime
from money import Money
from catalog.products import AbstractProduct, BookProduct, ClothingProduct, ElectronicProduct, ValidationError


class IValidator(Protocol):
    def validate(self, attrs: dict[str, Any]) -> None: ...

class IIndexMapper(Protocol):
    def map(self, product: AbstractProduct) -> dict[str, Any]: ...

class ICategoryFamilyFactory(Protocol):
    def create_product(self, attrs: dict[str, Any]) -> AbstractProduct: ...
    def create_validator(self) -> IValidator: ...
    def create_index_mapper(self) -> IIndexMapper: ...

class ElectronicsValidator:
    def validate(self, attrs: dict[str, Any]) -> None:
        if "brand" not in attrs:
            raise ValidationError("Electronics must have a brand")

class SimpleIndexMapper:
    def map(self, product: AbstractProduct) -> dict[str, Any]:
        return {"id": str(product.get_id()), "title": product.get_title()}

class ElectronicsFamilyFactory:
    def create_product(self, attrs: dict[str, Any]) -> ElectronicProduct:
        v = self.create_validator()
        v.validate(attrs)
        money = Money(Decimal(attrs.get("price", "0.0")), attrs.get("currency", "USD"))
        return ElectronicProduct(attrs.get("title", "Unnamed"), money, attrs)

    def create_validator(self) -> IValidator:
        return ElectronicsValidator()

    def create_index_mapper(self) -> IIndexMapper:
        return SimpleIndexMapper()

class ClothingFamilyFactory:
    def create_product(self, attrs: dict[str, Any]) -> ClothingProduct:
        money = Money(Decimal(attrs.get("price", "0.0")), attrs.get("currency", "USD"))
        return ClothingProduct(attrs.get("title", "Unnamed"), money, attrs)

    def create_validator(self) -> IValidator:
        class _V:
            def validate(self, a: dict[str, Any]) -> None:
                if "size" not in a:
                    raise ValidationError("Clothing must have size")
        return _V()

    def create_index_mapper(self) -> IIndexMapper:
        return SimpleIndexMapper()

class BookFamilyFactory:
    def create_product(self, attrs: dict[str, Any]) -> BookProduct:
        money = Money(Decimal(attrs.get("price", "0.0")), attrs.get("currency", "USD"))
        return BookProduct(attrs.get("title", "Unnamed"), money, attrs)

    def create_validator(self) -> IValidator:
        class _V:
            def validate(self, a: dict[str, Any]) -> None:
                if "author" not in a:
                    raise ValidationError("Book must have author")
        return _V()

    def create_index_mapper(self) -> IIndexMapper:
        return SimpleIndexMapper()