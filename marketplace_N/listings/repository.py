from typing import Optional, Protocol
import uuid
from listings.models import Listing


class IListingRepository(Protocol):
    def save(self, listing: Listing) -> None: ...
    def find(self, id: uuid.UUID) -> Optional[Listing]: ...
    def update(self, id: uuid.UUID, listing: Listing) -> None: ...
    def delete(self, id: uuid.UUID) -> None: ...

class ListingRepository:
    def __init__(self):
        self._storage: dict[uuid.UUID, Listing] = {}

    def save(self, listing: Listing) -> None:
        self._storage[listing.id] = listing

    def find(self, id: uuid.UUID) -> Optional[Listing]:
        return self._storage.get(id)

    def update(self, id: uuid.UUID, listing: Listing) -> None:
        if id not in self._storage:
            raise KeyError("Listing not found")
        self._storage[id] = listing

    def delete(self, id: uuid.UUID) -> None:
        if id in self._storage:
            del self._storage[id]

class ListingRepositoryCacheProxy(IListingRepository):
    def __init__(self, storage: ListingRepository):
        self._storage = storage
        self._cache: dict[uuid.UUID, Listing] = {}

    def find(self, id: uuid.UUID) -> Optional[Listing]:
        if id in self._cache:
            return self._cache[id]
        found = self._storage.find(id)
        if found:
            self._cache[id] = found
        return found

    def save(self, listing: Listing) -> None:
        self._storage.save(listing)
        self._cache[listing.id] = listing

    def update(self, id: uuid.UUID, listing: Listing) -> None:
        self._storage.update(id, listing)
        self._cache[id] = listing

    def delete(self, id: uuid.UUID) -> None:
        self._storage.delete(id)
        self._cache.pop(id, None)