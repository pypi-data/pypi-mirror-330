# ───────────────────────────────────────────────────── imports ────────────────────────────────────────────────────── #
from pydantic.v1.utils import to_lower_camel as pydantic_lower_camel

# ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────── #
#                           specifies all modules that shall be loaded and imported into the                           #
#                                current namespace when we use 'from package import *'                                 #
# ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────── #

__all__ = ["is_camel_case", "to_lower_camel"]


def is_camel_case(value: str) -> bool:
    return value != value.lower() and value != value.upper() and "_" not in value


def to_lower_camel(value: str) -> str:
    """Returns the value in lower camel case.

    e.g. camelCase

    """
    return value if is_camel_case(value=value) else pydantic_lower_camel(value)
