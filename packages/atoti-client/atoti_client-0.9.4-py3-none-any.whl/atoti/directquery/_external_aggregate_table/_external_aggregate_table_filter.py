from __future__ import annotations

from typing import Literal, TypeAlias

from ..._constant import Constant
from ..._identification import ColumnIdentifier
from ..._operation import IsInCondition, LogicalCondition, RelationalCondition

_ExternalAggregateTableLeafFilter: TypeAlias = (
    IsInCondition[ColumnIdentifier, Literal["IS_IN"], Constant]
    | RelationalCondition[ColumnIdentifier, Literal["EQ"], Constant]
)
ExternalAggregateTableFilter: TypeAlias = (
    _ExternalAggregateTableLeafFilter
    | LogicalCondition[_ExternalAggregateTableLeafFilter, Literal["AND"]]
)
