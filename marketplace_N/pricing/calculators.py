from decimal import Decimal
from typing import Any, Protocol

from listings.models import Listing
from money import Money


class IPriceCalculator(Protocol):
    def calculate(self, listing: Listing, ctx: dict[str, Any]) -> Money: ...

class BasePriceCalculator:
    def calculate(self, listing: Listing, ctx: dict[str, Any]) -> Money:
        # assume 'price' is in payload
        p = listing.payload.get("price")
        if isinstance(p, str):
            return Money(Decimal(p), listing.payload.get("currency", "USD"))
        if isinstance(p, Money):
            return p
        return Money(Decimal("0.0"), "USD")

class PromotionDecorator(IPriceCalculator):
    def __init__(self, next_calc: IPriceCalculator):
        self._next = next_calc

    def calculate(self, listing: Listing, ctx: dict[str, Any]) -> Money:
        base = self._next.calculate(listing, ctx)
        discount = ctx.get("promotion_discount", Decimal("0.0"))
        if isinstance(discount, Decimal):
            return Money(base.amount - discount, base.currency)
        return base

class TaxDecorator(IPriceCalculator):
    def __init__(self, next_calc: IPriceCalculator, tax_rate: float):
        self._next = next_calc
        self.tax_rate = Decimal(str(tax_rate))

    def calculate(self, listing: Listing, ctx: dict[str, Any]) -> Money:
        base = self._next.calculate(listing, ctx)
        taxed = base.amount * (Decimal("1.0") + self.tax_rate)
        return Money(taxed, base.currency)

class LoyaltyDecorator(IPriceCalculator):
    def __init__(self, next_calc: IPriceCalculator, loyalty_level: str):
        self._next = next_calc
        self.loyalty_level = loyalty_level

    def calculate(self, listing: Listing, ctx: dict[str, Any]) -> Money:
        base = self._next.calculate(listing, ctx)
        if self.loyalty_level == "GOLD":
            return Money(base.amount * Decimal("0.9"), base.currency)
        return base