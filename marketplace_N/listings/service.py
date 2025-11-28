from datetime import datetime
from typing import Optional
import uuid
from catalog.registry import CategoryRegistry
from listings.dto import ListingDTO
from listings.models import Listing
from listings.repository import IListingRepository


class ListingService:
    def __init__(self, registry: CategoryRegistry, repo: IListingRepository):
        self._registry = registry
        self._repo = repo

    def create_listing(self, dto: ListingDTO) -> Listing:
        factory = self._registry.get_factory(dto.category_code)
        attrs = dict(dto.attributes)
        attrs["price"] = str(dto.price.amount)
        attrs["currency"] = dto.price.currency
        attrs["title"] = dto.title
        product = factory.create_product(attrs)
        listing = Listing(id=uuid.uuid4(),
                          product_type=product.__class__.__name__,
                          payload=product.get_attributes(),
                          created_at=datetime.utcnow(), seller_id=dto.seller_id)
        self._repo.save(listing)
        return listing

    def get_listing(self, id: uuid.UUID) -> Optional[Listing]:
        return self._repo.find(id)

    def update_listing(self, id: uuid.UUID, dto: ListingDTO) -> Listing:
        found = self._repo.find(id)
        if not found:
            raise KeyError("Listing not found")
        # replace payload minimally
        found.payload.update(dto.attributes)
        self._repo.update(id, found)
        return found

    def delete_listing(self, id: uuid.UUID) -> None:
        self._repo.delete(id)