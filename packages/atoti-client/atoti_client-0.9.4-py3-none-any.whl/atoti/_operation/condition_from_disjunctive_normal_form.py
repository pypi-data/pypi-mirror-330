from collections.abc import Sequence
from typing import Literal, overload

from .operation import (
    LogicalCondition,
    LogicalConditionLeafOperandT_co,
    LogicalConditionOperatorBound,
    LogicalConditionOperatorT_co,
    OtherLogicalConditionOperatorT,
)


def _combine(
    *conditions: LogicalConditionLeafOperandT_co
    | LogicalCondition[LogicalConditionLeafOperandT_co, LogicalConditionOperatorT_co],
    operator: OtherLogicalConditionOperatorT,
) -> (
    LogicalConditionLeafOperandT_co
    | LogicalCondition[
        LogicalConditionLeafOperandT_co,
        LogicalConditionOperatorBound | OtherLogicalConditionOperatorT,
    ]
):
    if not conditions:
        raise ValueError("No conditions to combine.")

    iterator = iter(conditions)
    condition = next(iterator)

    if len(conditions) == 1:
        return condition

    return LogicalCondition(
        operands=(
            condition,
            _combine(*iterator, operator=operator),
        ),
        operator=operator,
    )


@overload
def condition_from_disjunctive_normal_form(
    leave_conditions: tuple[tuple[LogicalConditionLeafOperandT_co]],
    /,
) -> LogicalConditionLeafOperandT_co: ...


@overload
def condition_from_disjunctive_normal_form(  # type: ignore[overload-overlap]
    leave_conditions: tuple[Sequence[LogicalConditionLeafOperandT_co]],
    /,
) -> (
    LogicalConditionLeafOperandT_co
    | LogicalCondition[LogicalConditionLeafOperandT_co, Literal["AND"]]
): ...


@overload
def condition_from_disjunctive_normal_form(
    leave_conditions: Sequence[tuple[LogicalConditionLeafOperandT_co]],
    /,
) -> (
    LogicalConditionLeafOperandT_co
    | LogicalCondition[LogicalConditionLeafOperandT_co, Literal["OR"]]
): ...


@overload
def condition_from_disjunctive_normal_form(
    leave_conditions: Sequence[Sequence[LogicalConditionLeafOperandT_co]],
    /,
) -> (
    LogicalConditionLeafOperandT_co
    | LogicalCondition[LogicalConditionLeafOperandT_co, LogicalConditionOperatorBound]
): ...


def condition_from_disjunctive_normal_form(
    leave_conditions: Sequence[Sequence[LogicalConditionLeafOperandT_co]],
    /,
) -> (
    LogicalConditionLeafOperandT_co
    | LogicalCondition[LogicalConditionLeafOperandT_co, LogicalConditionOperatorBound]
):
    """Return a single condition from leave conditions in disjunctive normal form (DNF).

    For example: ``((foo, bar), (foo, baz))`` will return ``foo & (bar | baz)``.
    """
    return _combine(
        *(
            _combine(*conjunct_conditions, operator="AND")
            for conjunct_conditions in leave_conditions
        ),
        operator="OR",
    )
