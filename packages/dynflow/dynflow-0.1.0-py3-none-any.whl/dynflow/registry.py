from typing import Any, Callable, Dict, Tuple, Type, TypeVar

T = TypeVar("T")


class Registry:
    _name: str
    _protocol_class: Type[T]
    _registry: Dict[str, Type[T]]

    def __init__(self, name: str, protocol_class: Type[T]):
        self._name = name
        self._protocol_class = protocol_class
        self._registry = {}

    def register(self, component_name: str) -> Callable[[Type[T]], Type[T]]:
        def decorator(component_class: Any) -> Type[T]:
            if not issubclass(component_class, self._protocol_class):
                raise ValueError("Invalid Component Class")
            if component_name in self._registry:
                raise ValueError(f"Component name '{component_name}' is already registered in {self._name}")

            self._registry[component_name] = component_class
            return component_class

        return decorator

    @property
    def is_empty(self) -> bool:
        return not bool(self._registry)

    def get_component(self, component_name: str, *args: Tuple[Any], **kwargs: Any) -> T:
        if self.is_empty:
            raise ValueError(f"No components registered in the registry {self._name}")
        component_class = self._registry.get(component_name)
        if component_class is None:
            raise ValueError(f"Unknown Component: {component_name}")
        return component_class(*args, **kwargs)

    def purge(self) -> None:
        self._registry.clear()
