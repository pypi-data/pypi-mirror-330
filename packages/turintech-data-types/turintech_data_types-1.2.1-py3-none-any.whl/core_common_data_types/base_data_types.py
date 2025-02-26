# ───────────────────────────────────────────────────── imports ────────────────────────────────────────────────────── #
from typing_extensions import TypeAlias

from core_common_data_types.base_data_types_tos import CamelCaseBaseModelWithExtra

# ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────── #
#                           specifies all modules that shall be loaded and imported into the                           #
#                                current namespace when we use 'from package import *'                                 #
# ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────── #

__all__ = ["CamelCaseModelWithExtra"]

# DEPRECATED => Keep until we are sure to replace all its references
CamelCaseModelWithExtra: TypeAlias = CamelCaseBaseModelWithExtra
