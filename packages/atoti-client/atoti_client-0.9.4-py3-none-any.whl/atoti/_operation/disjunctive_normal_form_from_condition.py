from itertools import chain
from typing import Literal, overload

from .operation import (
    ConditionBound,
    LogicalCondition,
    LogicalConditionLeafOperandBound,
    LogicalConditionLeafOperandT_co,
    LogicalConditionOperatorBound,
)


@overload
def disjunctive_normal_form_from_condition(
    condition: LogicalConditionLeafOperandT_co,  # type: ignore[misc]
    /,
) -> tuple[tuple[LogicalConditionLeafOperandT_co]]: ...


@overload
def disjunctive_normal_form_from_condition(  # type: ignore[overload-overlap] # pyright: ignore[reportOverlappingOverload]
    condition: LogicalConditionLeafOperandT_co
    | LogicalCondition[LogicalConditionLeafOperandT_co, Literal["AND"]],
    /,
) -> tuple[tuple[LogicalConditionLeafOperandT_co, ...]]: ...


@overload
def disjunctive_normal_form_from_condition(
    condition: LogicalConditionLeafOperandT_co
    | LogicalCondition[LogicalConditionLeafOperandT_co, Literal["OR"]],
    /,
) -> tuple[tuple[LogicalConditionLeafOperandT_co], ...]: ...


@overload
def disjunctive_normal_form_from_condition(
    condition: LogicalConditionLeafOperandT_co
    | LogicalCondition[LogicalConditionLeafOperandT_co, LogicalConditionOperatorBound],
    /,
) -> tuple[tuple[LogicalConditionLeafOperandT_co], ...]: ...


def disjunctive_normal_form_from_condition(
    condition: ConditionBound,
    /,
) -> tuple[tuple[LogicalConditionLeafOperandBound, ...], ...]:
    """Decombine the passed condition into leave conditions in disjunctive normal form (DNF).

    For example: ``foo & (bar | baz)`` will return ``((foo, bar), (foo, baz))``.
    """
    if not isinstance(condition, LogicalCondition):
        return ((condition,),)

    first_dnf, second_dnf = (
        disjunctive_normal_form_from_condition(operand)
        for operand in condition.operands
    )

    match condition.operator:
        case "AND":
            return tuple(
                tuple(chain(first, second))
                for first in first_dnf
                for second in second_dnf
            )
        case "OR":
            return first_dnf + second_dnf
