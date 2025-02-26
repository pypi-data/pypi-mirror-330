# ───────────────────────────────────────────────────── imports ────────────────────────────────────────────────────── #
from enum import Enum
from pathlib import Path
from typing import Dict, List, Literal, TypeVar, Union

from evoml_api_models import BaseDefaultConf, BaseModelWithAlias, PropertyBaseModel
from pydantic.v1 import BaseModel, BaseSettings
from typing_extensions import TypeAlias

# ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────── #
#                           specifies all modules that shall be loaded and imported into the                           #
#                                current namespace when we use 'from package import *'                                 #
# ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────── #

__all__ = [
    "PathType",
    "DataModelType",
    "JsonType",
    "DictType",
    "GenericT",
    "EnumT",
    "DataModelT",
    "JsonT",
    "DictT",
    "BaseModelT",
    "BaseSettingsT",
    "BaseDefaultConfT",
    "PositionType",
]

# ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────── #
#                                                      Data types                                                      #
# ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────── #

PathType: TypeAlias = Union[str, Path]

DataModelType: TypeAlias = Union[BaseModel, List[BaseModel], BaseModelWithAlias, List[BaseModelWithAlias]]
JsonType: TypeAlias = Union[Dict, List[Dict]]
DictType: TypeAlias = Union[Dict, BaseModel, BaseSettings, PropertyBaseModel, BaseModelWithAlias]

# ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────── #
#                                                    Generic Types                                                     #
# ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────── #

GenericT = TypeVar("GenericT")
EnumT = TypeVar("EnumT", bound=Enum)

DataModelT = TypeVar("DataModelT", bound=DataModelType)
JsonT = TypeVar("JsonT", bound=JsonType)
DictT = TypeVar("DictT", bound=DictType)

BaseModelT = TypeVar("BaseModelT", bound=BaseModel)
BaseSettingsT = TypeVar("BaseSettingsT", bound=BaseSettings)
BaseDefaultConfT = TypeVar("BaseDefaultConfT", bound=BaseDefaultConf)

# ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────── #
#                                                     Filter types                                                     #
# ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────── #

PositionType: TypeAlias = Literal["oldest", "latest"]
