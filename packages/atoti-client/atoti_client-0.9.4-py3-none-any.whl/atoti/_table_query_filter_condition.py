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

_TableQueryFilterLeafCondition: TypeAlias = (
    IsInCondition[ColumnIdentifier, Literal["IS_IN"], Constant]
    | RelationalCondition[
        ColumnIdentifier,
        RelationalConditionOperatorBound,
        Constant,
    ]
)
TableQueryFilterCondition: TypeAlias = (
    _TableQueryFilterLeafCondition
    | LogicalCondition[_TableQueryFilterLeafCondition, LogicalConditionOperatorBound]
)
