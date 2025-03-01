# ruff: noqa: ARG002 PT009 PT027 SLF001

import json
import unittest
from pathlib import Path
from typing import Any, Dict, Tuple

from dynflow.config import Config
from example.base import registry
from example.pipeline import Pipeline


class TestPipeline(unittest.TestCase):
    def setUp(self) -> None:
        # Register components using the registry decorator
        @registry.register("component1")
        class Component1:
            def run(self, *args: Tuple[Any], **kwargs: Dict[str, Any]) -> Any:
                return "Result from Component1"

        @registry.register("component2")
        class Component2:
            def run(self, *args: Tuple[Any], **kwargs: Dict[str, Any]) -> Any:
                return "Result from Component2"

        self.json_data = {
            "pipeline": {"components": ["Component1", "Component2"]},
            "component.Component1": {"factory": "component1", "init_args": {}, "run_args": {}},
            "component.Component2": {"factory": "component2", "init_args": {}, "run_args": {}},
        }
        # Create a sample config
        self.config = Config(**self.json_data)

        with open("test.json", "w") as f:
            json.dump(self.json_data, f)

    def tearDown(self) -> None:
        Path("test.json").unlink()
        registry.purge()

    def test_pipeline_initialization(self) -> None:
        pipeline = Pipeline.from_config(self.config)
        self.assertEqual(len(pipeline._components), 2)
        self.assertEqual(pipeline.component_names, ["Component1", "Component2"])

    def test_pipeline_run(self) -> None:
        pipeline = Pipeline.from_config(self.config)
        pipeline.run()
        # Assuming the components have a run method that can be checked
        for name, component, _, _ in pipeline._components:
            self.assertEqual(component.run(), f"Result from {name}")

    def test_pipeline_load(self) -> None:
        pipeline = Pipeline.load("test.json")
        self.assertEqual(len(pipeline._components), 2)
        self.assertEqual(pipeline.component_names, ["Component1", "Component2"])

    def test_pipeline_add_component(self) -> None:
        pipeline = Pipeline()
        pipeline.add_component(self.config["component.Component1"], "Component1")
        self.assertEqual(len(pipeline._components), 1)
        self.assertEqual(pipeline.component_names, ["Component1"])


if __name__ == "__main__":
    unittest.main()
