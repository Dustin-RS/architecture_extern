from __future__ import annotations
from dataclasses import dataclass, field
from decimal import Decimal
from typing import Any, List, Optional, Protocol, runtime_checkable
from abc import ABC, abstractmethod
import uuid
from datetime import datetime

@dataclass(frozen=True)
class Money:
    amount: Decimal
    currency: str = "USD"

    def __add__(self, other: "Money") -> "Money":
        if self.currency != other.currency:
            raise ValueError("Different currencies")
        return Money(self.amount + other.amount, self.currency)

    def __mul__(self, qty: int) -> "Money":
        return Money(self.amount * Decimal(qty), self.currency)
