from typing import Literal, TypeAlias

from ._operation import HierarchyIsInConditionBound, LogicalCondition

_CubeMaskLeafCondition: TypeAlias = HierarchyIsInConditionBound

CubeMaskCondition: TypeAlias = (
    _CubeMaskLeafCondition | LogicalCondition[_CubeMaskLeafCondition, Literal["AND"]]
)
