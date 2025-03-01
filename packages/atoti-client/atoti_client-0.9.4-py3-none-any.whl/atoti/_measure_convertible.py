from __future__ import annotations

from typing import Literal

from typing_extensions import TypeIs

from ._constant import Constant, ConstantValue
from ._identification import (
    HasIdentifier,
    HierarchyIdentifier,
    LevelIdentifier,
    MeasureIdentifier,
)
from ._operation import (
    Condition,
    ConditionBound,
    HierarchyIsInCondition,
    IsInCondition,
    LogicalCondition,
    LogicalConditionOperatorBound,
    Operation,
    OperationBound,
    RelationalCondition,
    RelationalConditionOperatorBound,
)

MeasureConvertibleIdentifier = HierarchyIdentifier | LevelIdentifier | MeasureIdentifier

MeasureOperation = Operation[MeasureConvertibleIdentifier]

_MeasureLeafCondition = (
    HierarchyIsInCondition[Literal["IS_IN"]]
    | IsInCondition[
        LevelIdentifier | MeasureIdentifier, Literal["IS_IN"], Constant | None
    ]
    | RelationalCondition[
        LevelIdentifier | MeasureIdentifier | MeasureOperation,
        RelationalConditionOperatorBound,
        Constant | MeasureConvertibleIdentifier | MeasureOperation | None,
    ]
)
MeasureCondition = (
    _MeasureLeafCondition
    | LogicalCondition[_MeasureLeafCondition, LogicalConditionOperatorBound]
)

VariableMeasureOperand = (
    MeasureCondition | MeasureOperation | MeasureConvertibleIdentifier
)
MeasureOperand = Constant | VariableMeasureOperand

VariableMeasureConvertible = (
    HasIdentifier[MeasureConvertibleIdentifier] | MeasureCondition | MeasureOperation
)
MeasureConvertible = ConstantValue | VariableMeasureConvertible


def _is_measure_base_operation(value: ConditionBound | OperationBound, /) -> bool:
    # It is not a measure `BaseOperation` if there are some unexpected identifier types.
    return not (
        value._identifier_types
        - {HierarchyIdentifier, LevelIdentifier, MeasureIdentifier}
    )


def is_measure_condition(value: object, /) -> TypeIs[MeasureCondition]:
    return isinstance(value, Condition) and _is_measure_base_operation(value)


def is_measure_operation(value: object, /) -> TypeIs[MeasureOperation]:
    return isinstance(value, Operation) and _is_measure_base_operation(value)


def is_measure_condition_or_operation(
    value: object,
    /,
) -> TypeIs[MeasureCondition | MeasureOperation]:
    return (
        is_measure_condition(value)
        if isinstance(value, Condition)
        else is_measure_operation(value)
    )


def is_variable_measure_convertible(
    value: object,
    /,
) -> TypeIs[VariableMeasureConvertible]:
    return (
        isinstance(
            value._identifier,
            HierarchyIdentifier | LevelIdentifier | MeasureIdentifier,
        )
        if isinstance(value, HasIdentifier)
        else is_measure_condition_or_operation(value)
    )
