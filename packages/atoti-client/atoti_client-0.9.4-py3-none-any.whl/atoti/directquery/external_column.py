from __future__ import annotations

from collections.abc import Callable
from typing import Final, Literal, final, overload

from typing_extensions import override

from .._constant import Constant, ConstantValue
from .._data_type import DataType
from .._identification import ColumnName, ExternalColumnIdentifier
from .._operation import (
    IsInCondition,
    OperandConvertibleWithIdentifier,
    RelationalCondition,
)


@final
class ExternalColumn(OperandConvertibleWithIdentifier[ExternalColumnIdentifier]):
    """Column of an external table."""

    def __init__(
        self,
        identifier: ExternalColumnIdentifier,
        /,
        *,
        get_data_type: Callable[[], DataType],
    ) -> None:
        self._get_data_type: Final = get_data_type
        self.__identifier: Final = identifier

    @property
    def name(self) -> ColumnName:
        """The name of the column."""
        return self._identifier.column_name

    @property
    def data_type(self) -> DataType:
        """The type of the elements in the column."""
        return self._get_data_type()

    @property
    @override
    def _identifier(self) -> ExternalColumnIdentifier:
        return self.__identifier

    @property
    @override
    def _operation_operand(self) -> ExternalColumnIdentifier:
        return self._identifier

    @overload
    def isin(
        self,
        *elements: ConstantValue,
    ) -> (
        IsInCondition[ExternalColumnIdentifier, Literal["IS_IN"], Constant]
        | RelationalCondition[ExternalColumnIdentifier, Literal["EQ"], Constant]
    ): ...

    @overload
    def isin(
        self,
        *elements: ConstantValue | None,
    ) -> (
        IsInCondition[
            ExternalColumnIdentifier,
            Literal["IS_IN"],
            Constant | None,
        ]
        | RelationalCondition[ExternalColumnIdentifier, Literal["EQ"], Constant | None]
    ): ...

    def isin(
        self,
        *elements: ConstantValue | None,
    ) -> (
        IsInCondition[ExternalColumnIdentifier, Literal["IS_IN"], Constant | None]
        | RelationalCondition[ExternalColumnIdentifier, Literal["EQ"], Constant | None]
    ):
        """Return a condition evaluating to ``True`` if a column element is among the given elements and ``False`` otherwise.

        ``table["City"].isin("Paris", "New York")`` is equivalent to ``(table["City"] == "Paris") | (table["City"] == "New York")``.

        Args:
            elements: One or more elements on which the column should be.
        """
        return IsInCondition.of(
            subject=self._operation_operand,
            operator="IS_IN",
            elements={
                None if element is None else Constant.of(element)
                for element in elements
            },
        )
