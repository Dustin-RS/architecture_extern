from catalog.factories import ICategoryFamilyFactory


class CategoryRegistry:
    def __init__(self):
        self._factories: dict[str, ICategoryFamilyFactory] = {}

    def register_factory(self, code: str, f: ICategoryFamilyFactory) -> None:
        self._factories[code] = f

    def get_factory(self, code: str) -> ICategoryFamilyFactory:
        if code not in self._factories:
            raise KeyError(f"Factory {code} not registered")
        return self._factories[code]