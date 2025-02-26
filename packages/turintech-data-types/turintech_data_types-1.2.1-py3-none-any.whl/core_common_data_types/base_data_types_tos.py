# pylint: disable=useless-parent-delegation,bad-classmethod-argument
# ───────────────────────────────────────────────────── imports ────────────────────────────────────────────────────── #
from typing import Any, Dict, Set, TypeVar

from pydantic.v1 import BaseModel
from pydantic.v1.fields import ModelField

from core_common_data_types.base_data_types_dtos import ExcludeUnsetBaseModel, UpdateBaseModel
from core_common_data_types.utils_data_types_tos import to_lower_camel

# ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────── #
#                           specifies all modules that shall be loaded and imported into the                           #
#                                current namespace when we use 'from package import *'                                 #
# ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────── #

__all__ = [
    "CamelCaseBaseModel",
    "CamelCaseBaseModelWithExtra",
    "CamelCaseExcludeUnsetBaseModel",
    "CamelCaseUpdateBaseModel",
    "CamelCaseBaseModelT",
    "CamelCaseBaseModelWithExtraT",
    "CamelCaseExcludeUnsetBaseModelT",
    "CamelCaseUpdateBaseModelT",
]


class CamelCaseBaseModel(BaseModel):
    """Base Model with enabled alias.

    Whether an aliased field may be populated by its name as given by the model attribute, as well as the alias.

    """

    def dict(self, *args, by_alias: bool = True, **kwargs) -> Dict:
        """
        Generate a dictionary representation of the model, whose keys follow the JSON convention, optionally specifying
        which fields to include or exclude.
        """
        return super().dict(by_alias=by_alias, *args, **kwargs)

    def dict_py(self, *args, **kwargs):
        """Gets the dictionary whose keys follow the Python convention.

        It is the same behavior as the dict() method but with a more descriptive name.     {         "snake_case_key":
        value     }

        """
        if kwargs and "by_alias" in kwargs:
            kwargs.pop("by_alias", None)
        return super().dict(by_alias=False, *args, **kwargs)

    def dict_json(self, *args, **kwargs):
        """Gets the dictionary whose keys follow the JSON convention by ensuring that 'aliases' are used as keys:
        {
            "camelCaseKey": value
        }
        """
        if kwargs and "by_alias" in kwargs:
            kwargs.pop("by_alias", None)
        return super().dict(by_alias=True, *args, **kwargs)

    def update(self, data: Dict[str, object]) -> None:
        # Data update
        for key, field in self.__fields__.items():
            if key in data or field.alias in data:
                setattr(self, key, data.get(key, data.get(field.alias)))
        # Data Validation
        self.__class__(**self.dict())

    @classmethod
    def get_field(cls, field_name: str, values: Dict) -> Any:
        """Retrieve the value of the field from the given dictionary searching by the field name and its alias.

        If exist a value for the field name and the alias, it will return the field name value

        """
        field: ModelField = cls.__fields__[field_name]
        return values.get(field.name, values.get(field.alias))

    class Config:
        """
        Class with base attributes for configuration.
        """

        extra = "ignore"

        # Use aliases in the JSON serialization in camel case instead of snake case
        alias_generator = to_lower_camel

        # Recognizes both original name and alias as input
        allow_population_by_field_name = True


class CamelCaseBaseModelWithExtra(CamelCaseBaseModel, extra="allow"):
    """Base Model with enabled alias for extra fields.

    Whether an aliased field may be populated by its name as given by the model attribute, as well as the alias.

    """

    @property
    def extra_fields(self) -> Set[str]:
        return set(self.__dict__) - set(self.__fields__)

    def dict(self, *args, by_alias: bool = True, **kwargs) -> Dict:
        data = super().dict(by_alias=by_alias, *args, **kwargs)
        if by_alias:
            for field in self.extra_fields:
                data[to_lower_camel(field)] = data.pop(field)
        return data


class CamelCaseExcludeUnsetBaseModel(CamelCaseBaseModel, ExcludeUnsetBaseModel):
    """
    Base model for TOs to return only the data that has been set.
    """


class CamelCaseUpdateBaseModel(CamelCaseBaseModel, UpdateBaseModel):  # type:ignore[misc]
    """Base model for updating TOs data.

    By making information update data models extend from this data model, it makes it easier to distinguish the
    fields that the user has actually modified (`exclude_unset`=True) from those that the user has not indicated.

    """


# ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────── #
#                                                    Generic Types                                                     #
# ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────── #

CamelCaseBaseModelT = TypeVar("CamelCaseBaseModelT", bound=CamelCaseBaseModel)
CamelCaseBaseModelWithExtraT = TypeVar("CamelCaseBaseModelWithExtraT", bound=CamelCaseBaseModelWithExtra)
CamelCaseExcludeUnsetBaseModelT = TypeVar("CamelCaseExcludeUnsetBaseModelT", bound=CamelCaseExcludeUnsetBaseModel)
CamelCaseUpdateBaseModelT = TypeVar("CamelCaseUpdateBaseModelT", bound=CamelCaseUpdateBaseModel)
