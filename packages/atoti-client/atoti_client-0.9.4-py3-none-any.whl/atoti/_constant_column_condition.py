from __future__ import annotations

from typing import Literal, TypeAlias

from ._constant import Constant
from ._identification import ColumnIdentifier
from ._operation import (
    IsInCondition,
    LogicalCondition,
    LogicalConditionOperatorBound,
    RelationalCondition,
    RelationalConditionOperatorBound,
)

ConstantColumnLeafCondition: TypeAlias = (
    IsInCondition[ColumnIdentifier, Literal["IS_IN"], Constant | None]
    | RelationalCondition[
        ColumnIdentifier, RelationalConditionOperatorBound, Constant | None
    ]
)
ConstantColumnCondition: TypeAlias = (
    ConstantColumnLeafCondition
    | LogicalCondition[ConstantColumnLeafCondition, LogicalConditionOperatorBound]
)
