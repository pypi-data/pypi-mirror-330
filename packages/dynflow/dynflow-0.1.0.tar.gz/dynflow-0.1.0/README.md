## Creating a Registry

To create a registry follow the example below:

```python
from typing import Any, Dict, Protocol, Tuple, runtime_checkable

from dynflow import Registry


@runtime_checkable
class BaseComponent(Protocol):
    def run(self, args: Tuple[Any], **kwargs: Dict[str, Any]) -> Any: ...


registry = Registry("ComponentRegistry", BaseComponent)
```

## How to Register Componnets

```python

from file1.py import registry

@registry.register('MyComponent1')
class MyComponent1:
    def run(self, args: Tuple[Any], **kwargs: Dict[str, Any]) -> Any:
        print("Running MyComponent with args:", args, "and kwargs:", kwargs)


@registry.register('MyComponent2')
class MyComponent2:
    def run(self, args: Tuple[Any], **kwargs: Dict[str, Any]) -> Any:
        print("Running MyComponent with args:", args, "and kwargs:", kwargs)        
```


## Config File Examples

1. JSON Format
   See [config.json](example/config.json) for an example of a JSON configuration file.

2. YAML Format
   See [config.yml](example/config.yml) for an example of a YAML configuration file.

3. CFG Format
   See [config.cfg](example/config.cfg) for an example of a CFG configuration file.

## For building build Pipeline from list of components use [example](example/pipeline.py)


## How to maintain
1. Running unit-tests `python -m unittest discover -s tests` 
2. Removing Cache files `pyclean -d jupyter package ruff -v .`
   