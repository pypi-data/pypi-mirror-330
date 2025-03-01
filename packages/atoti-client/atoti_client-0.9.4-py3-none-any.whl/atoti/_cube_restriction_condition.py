from __future__ import annotations

from typing import Literal, TypeAlias

from ._constant import Constant
from ._identification import LevelIdentifier
from ._operation.operation import (
    IsInCondition,
    LogicalCondition,
    RelationalCondition,
)

_CubeRestrictionLeafCondition: TypeAlias = (
    IsInCondition[
        LevelIdentifier,
        Literal["IS_IN"],
        Constant,
    ]
    | RelationalCondition[
        LevelIdentifier,
        Literal["EQ"],
        Constant,
    ]
)
CubeRestrictionCondition: TypeAlias = (
    _CubeRestrictionLeafCondition
    | LogicalCondition[_CubeRestrictionLeafCondition, Literal["AND"]]
)
