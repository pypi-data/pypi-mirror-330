# ruff: noqa: ARG002 PT009 PT027
import unittest
from typing import Any, Dict, Protocol, Tuple, runtime_checkable

from dynflow.registry import Registry


@runtime_checkable
class BaseComponent(Protocol):
    def __call__(self, *args: Tuple[Any], **kwargs: Dict[str, Any]) -> Any: ...


class TestRegistry(unittest.TestCase):
    def setUp(self) -> None:
        self.registry = Registry("TestRegistry", BaseComponent)

        @self.registry.register("component1")
        class Component1:
            def __call__(self, *args: Tuple[Any], **kwargs: Dict[str, Any]) -> Any:
                return "Result from Component1"

    def tearDown(self) -> None:
        self.registry.purge()

    def test_register_and_get_component(self) -> None:
        component = self.registry.get_component("component1")
        result = component()
        self.assertEqual(result, "Result from Component1")

    def test_register_invalid_component(self) -> None:
        with self.assertRaises(ValueError):

            @self.registry.register("invalid_component")
            class InvalidComponent:
                pass

    def test_register_duplicate_component(self) -> None:
        with self.assertRaises(ValueError):

            @self.registry.register("component1")
            class DuplicateComponent2:
                def __call__(self, *args: Tuple[Any], **kwargs: Dict[str, Any]) -> Any:
                    return "Result from DuplicateComponent2"

    def test_get_unknown_component(self) -> None:
        with self.assertRaises(ValueError):
            self.registry.get_component("UnknownComponent")


if __name__ == "__main__":
    unittest.main()
