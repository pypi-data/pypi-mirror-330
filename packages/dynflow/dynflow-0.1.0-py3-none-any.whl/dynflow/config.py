import ast
import json
from configparser import ConfigParser
from pathlib import Path
from types import MappingProxyType
from typing import Any, Dict, Mapping, Union

import yaml

from .registry import Registry


class Config(dict[str, Any]):
    def __init__(self, **kwargs: Any):
        super().__init__(**kwargs)
        self.validate()

    def validate(self) -> None:
        for key, value in self.items():
            if key == "pipeline":
                if "components" not in value or not isinstance(value["components"], list):
                    raise ValueError(f"{key} must contain 'components' as a list {value}")
                for name in value["components"]:
                    if f"component.{name}" not in self:
                        raise ValueError(f"Component {name!r} not found in config")
            elif key.startswith("component."):
                if "factory" not in value:
                    raise ValueError(f"Component {key} does not contain '@factory' key")
            else:
                raise ValueError(f"Key {key} does not start with 'component.'")

    def get_comp(self, compname: str) -> Dict:
        return self.get(f"component.{compname}")

    @classmethod
    def from_json(cls, path: Union[str, Path]) -> "Config":
        with open(path, "r") as f:
            data = json.load(f)
        return cls(**data)

    @classmethod
    def from_yml(cls, path: Union[str, Path]) -> "Config":
        with open(path, "r") as f:
            data = yaml.safe_load(f)
        return cls(**data)

    @classmethod
    def from_cfg(cls, path: Union[str, Path]) -> "Config":
        config_parser = ConfigParser()
        config_parser.read(path)

        data = {
            section: {k: ast.literal_eval(v) for k, v in config_parser[section].items()}
            for section in config_parser.sections()
        }

        return cls(**data)

    @classmethod
    def from_disk(cls, path: Union[str, Path]) -> "Config":
        if not isinstance(path, (Path, str)):
            raise ValueError("path should be of type str or Path")
        if str(path).endswith((".yaml", ".yml")):
            config = cls.from_yml(path)
        elif str(path).endswith((".json", ".JSON")):
            config = cls.from_json(path)
        elif str(path).endswith((".cfg", ".CFG")):
            config = cls.from_cfg(path)
        else:
            raise ValueError("Invalid file format")
        return config

    def copy(self) -> "Config":
        return Config(**self)

    def resolve(self, registry: Registry) -> Mapping[str, Any]:
        resolved_components = {}
        for key in self.keys():
            if key.startswith("component."):
                component_name = key.split("component.")[1]
                factory = self[key]["factory"]
                resolved_components[component_name] = registry.get_component(factory)
        return MappingProxyType(resolved_components)
