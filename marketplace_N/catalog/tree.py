from abc import ABC, abstractmethod

class CategoryComponent(ABC):
    def __init__(self, name: str):
        self._name = name

    def get_name(self) -> str:
        return self._name

    def get_children(self) -> list["CategoryComponent"]:
        return []

class CategoryLeaf(CategoryComponent):
    def __init__(self, name: str):
        super().__init__(name)

class CategoryComposite(CategoryComponent):
    def __init__(self, name: str):
        super().__init__(name)
        self._children: list[CategoryComponent] = []

    def add(self, component: CategoryComponent) -> None:
        self._children.append(component)

    def remove(self, component: CategoryComponent) -> None:
        self._children.remove(component)

    def get_children(self) -> list[CategoryComponent]:
        return list(self._children)
