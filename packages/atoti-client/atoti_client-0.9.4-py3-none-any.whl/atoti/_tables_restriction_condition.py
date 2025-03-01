from __future__ import annotations

from typing import Literal, TypeAlias

from ._constant import Constant
from ._identification import ColumnIdentifier
from ._operation import IsInCondition, LogicalCondition, RelationalCondition

_TablesRestrictionLeafCondition: TypeAlias = (
    IsInCondition[
        ColumnIdentifier,
        Literal["IS_IN"],
        Constant,
    ]
    | RelationalCondition[
        ColumnIdentifier,
        Literal["EQ"],
        Constant,
    ]
)
TablesRestrictionCondition: TypeAlias = (
    _TablesRestrictionLeafCondition
    | LogicalCondition[_TablesRestrictionLeafCondition, Literal["AND"]]
)
