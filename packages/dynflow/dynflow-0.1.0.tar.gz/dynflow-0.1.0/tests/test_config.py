# ruff: noqa: ARG002 PT009 PT027
import json
import unittest
from pathlib import Path

import yaml

from dynflow.config import Config


class TestConfig(unittest.TestCase):
    def setUp(self) -> None:
        self.json_data = {
            "component.ComponentAbc": {
                "factory": "component_abc",
                "arg1": "path/to/some/file",
            },
            "component.ComponentCdf": {"factory": "component_cdf"},
            "component.ComponentEfg": {"factory": "component_efg"},
            "component.ComponentHij": {"factory": "component_hij"},
            "component.ComponentXyz": {"factory": "component_xyz"},
            "pipeline": {
                "components": [
                    "ComponentAbc",
                    "ComponentCdf",
                    "ComponentEfg",
                    "ComponentHij",
                    "ComponentXyz",
                ]
            },
        }

        self.yaml_data = self.json_data

        self.cfg_data = self.cfg_data = """
                        [component.ComponentAbc]
                        factory = "component_abc"
                        arg1 = 'path/to/some/file'

                        [component.ComponentCdf]
                        factory = "component_cdf"

                        [component.ComponentEfg]
                        factory = "component_efg"

                        [component.ComponentHij]
                        factory = "component_hij"

                        [component.ComponentXyz]
                        factory = "component_xyz"

                        [pipeline]
                        components = ["ComponentAbc", "ComponentCdf", "ComponentEfg", "ComponentHij", "ComponentXyz"]
                        """

        with open("test.json", "w") as f:
            json.dump(self.json_data, f)

        with open("test.yaml", "w") as f:
            yaml.dump(self.yaml_data, f)

        with open("test.cfg", "w") as f:
            f.write(self.cfg_data)

    def tearDown(self) -> None:
        Path("test.json").unlink()
        Path("test.yaml").unlink()
        Path("test.cfg").unlink()

    def test_from_json(self) -> None:
        config = Config.from_json("test.json")
        self.assertEqual(config, self.json_data)
        config.validate()

    def test_from_yml(self) -> None:
        config = Config.from_yml("test.yaml")
        self.assertEqual(config, self.yaml_data)
        config.validate()

    def test_from_cfg(self) -> None:
        config = Config.from_cfg("test.cfg")
        self.assertEqual(config, self.json_data)
        config.validate()

    def test_from_disk_json(self) -> None:
        config = Config.from_disk("test.json")
        self.assertEqual(config, self.json_data)
        config.validate()

    def test_from_disk_yaml(self) -> None:
        config = Config.from_disk("test.yaml")
        self.assertEqual(config, self.yaml_data)
        config.validate()

    def test_from_disk_cfg(self) -> None:
        config = Config.from_disk("test.cfg")
        self.assertEqual(config, self.json_data)
        config.validate()

    def test_copy(self) -> None:
        config = Config(**self.json_data)
        config_copy = config.copy()
        self.assertEqual(config, config_copy)


if __name__ == "__main__":
    unittest.main()
