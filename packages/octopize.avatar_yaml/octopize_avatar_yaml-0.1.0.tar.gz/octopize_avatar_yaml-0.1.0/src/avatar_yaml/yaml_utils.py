from __future__ import annotations

from dataclasses import asdict
from enum import StrEnum

import yaml

DEFAULT_INDENT_WIDTH = 2

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from _typeshed import DataclassInstance

# Allows StrEnum to be serialized as a string
yaml.SafeDumper.add_multi_representer(
    StrEnum,
    yaml.representer.SafeRepresenter.represent_str,
)


def to_yaml(obj: DataclassInstance) -> str:
    """Convert an object to yaml."""
    return yaml.safe_dump(asdict(obj), indent=DEFAULT_INDENT_WIDTH)
