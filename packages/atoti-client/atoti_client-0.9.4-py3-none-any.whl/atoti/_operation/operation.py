from __future__ import annotations

import math
from abc import ABC, abstractmethod
from collections.abc import Mapping, Sequence, Set as AbstractSet
from dataclasses import KW_ONLY, dataclass as _dataclass
from itertools import chain
from typing import (
    Annotated,
    Generic,
    Literal,
    NoReturn,
    TypeAlias,
    TypeVar,
    Union,
    cast,
    final,
    overload,
)

from pydantic import AfterValidator, BaseModel, Field, SerializeAsAny
from pydantic.dataclasses import dataclass
from typing_extensions import override

from .._collections import FrozenSequence
from .._constant import Constant, ConstantValue
from .._identification import (
    HasIdentifier,
    HierarchyIdentifier,
    Identifier,
    IdentifierT_co,
    LevelIdentifier,
    LevelName,
)
from .._pydantic import PYDANTIC_CONFIG as _PYDANTIC_CONFIG
from ._arithmetic_operator import ArithmeticOperator
from ._is_in_operator import INVERSE_IS_IN_OPERATOR, IsInOperator
from ._logical_operator import LogicalOperator
from ._other_identifier import OtherIdentifierT_co
from .relational_operator import INVERSE_RELATIONAL_OPERATOR, RelationalOperator


@overload
def convert_to_operand(value: None, /) -> None: ...


@overload
def convert_to_operand(value: ConstantValue, /) -> Constant: ...


@overload
def convert_to_operand(value: HasIdentifier[IdentifierT_co], /) -> IdentifierT_co: ...


@overload
def convert_to_operand(
    value: OperandCondition[IdentifierT_co],
    /,
) -> OperandCondition[IdentifierT_co]: ...


@overload
def convert_to_operand(
    value: Operation[IdentifierT_co],
    /,
) -> Operation[IdentifierT_co]: ...


def convert_to_operand(
    value: OperandCondition[IdentifierT_co]
    | ConstantValue
    | HasIdentifier[IdentifierT_co]
    | Operation[IdentifierT_co]
    | None,
    /,
) -> Operand[IdentifierT_co] | None:
    if value is None or isinstance(value, Condition | Operation):
        return value
    if isinstance(value, HasIdentifier):
        return value._identifier
    return Constant.of(value)


class OperandConvertible(Generic[IdentifierT_co], ABC):
    @property
    @abstractmethod
    def _operation_operand(self) -> _UnconditionalVariableOperand[IdentifierT_co]: ...

    def isnull(
        self,
    ) -> RelationalCondition[
        _UnconditionalVariableOperand[IdentifierT_co], Literal["EQ"], None
    ]:
        """Return a condition evaluating to ``True`` when the element evaluates to ``None`` and ``False`` otherwise.

        Use `~obj.isnull()` for the opposite behavior.
        """
        return RelationalCondition(
            subject=self._operation_operand, operator="EQ", target=None
        )

    @final
    def __bool__(self) -> NoReturn:
        raise AssertionError(
            f"Instances of `{type(self).__name__}` cannot be cast to a boolean. Use a relational operator to create a condition instead.",
        )

    @override
    def __hash__(self) -> int:
        # The public API sometimes requires instances of this class to be used as mapping keys so they must be hashable.
        # However, these keys are only ever iterated upon (i.e. there is no get by key access) so the hash is not important.
        # The ID of the object is thus used, like `object.__hash__()` would do.
        return id(self)

    @final
    def __iter__(self) -> NoReturn:
        # Implementing this method and making it raise an error is required to avoid an endless loop when validating incorrect `AbstractSet`s with Pydantic.
        # For instance, without this, `tt.OriginScope(some_level)` never returns (`tt.OriginScope({some_level})` is the right code).
        # Making this method raise an error prevents Pydantic from calling `__getitem__()` which returns a new `IndexingOperation` instead of an attribute value.
        raise TypeError(f"Instances of {self.__class__.__name__} are not iterable.")

    @final
    def __getitem__(
        self,
        index: HasIdentifier[OtherIdentifierT_co]
        | Operation[OtherIdentifierT_co]
        | slice
        | int
        | Sequence[int],
        /,
    ) -> Operation[IdentifierT_co | OtherIdentifierT_co]:
        return IndexingOperation(
            self._operation_operand,
            index._identifier if isinstance(index, HasIdentifier) else index,
        )

    @override
    # The signature is not compatible with `object.__eq__()` on purpose.
    def __eq__(  # type: ignore[override] # pyright: ignore[reportIncompatibleMethodOverride]
        self,
        other: ConstantValue
        | HasIdentifier[OtherIdentifierT_co]
        | Operation[OtherIdentifierT_co],
        /,
    ) -> RelationalCondition[
        _UnconditionalVariableOperand[IdentifierT_co],
        Literal["EQ"],
        Constant | OtherIdentifierT_co | Operation[OtherIdentifierT_co],
    ]:
        assert other is not None, "Use `isnull()` instead."
        return RelationalCondition(
            subject=self._operation_operand,
            operator="EQ",
            target=convert_to_operand(other),
        )

    def __ge__(
        self,
        other: ConstantValue
        | HasIdentifier[OtherIdentifierT_co]
        | Operation[OtherIdentifierT_co],
        /,
    ) -> RelationalCondition[
        _UnconditionalVariableOperand[IdentifierT_co],
        Literal["GE"],
        Constant | OtherIdentifierT_co | Operation[OtherIdentifierT_co],
    ]:
        return RelationalCondition(
            subject=self._operation_operand,
            operator="GE",
            target=convert_to_operand(other),
        )

    def __gt__(
        self,
        other: ConstantValue
        | HasIdentifier[OtherIdentifierT_co]
        | Operation[OtherIdentifierT_co],
        /,
    ) -> RelationalCondition[
        _UnconditionalVariableOperand[IdentifierT_co],
        Literal["GT"],
        Constant | OtherIdentifierT_co | Operation[OtherIdentifierT_co],
    ]:
        return RelationalCondition(
            subject=self._operation_operand,
            operator="GT",
            target=convert_to_operand(other),
        )

    def __le__(
        self,
        other: ConstantValue
        | HasIdentifier[OtherIdentifierT_co]
        | Operation[OtherIdentifierT_co],
        /,
    ) -> RelationalCondition[
        _UnconditionalVariableOperand[IdentifierT_co],
        Literal["LE"],
        Constant | OtherIdentifierT_co | Operation[OtherIdentifierT_co],
    ]:
        return RelationalCondition(
            subject=self._operation_operand,
            operator="LE",
            target=convert_to_operand(other),
        )

    def __lt__(
        self,
        other: ConstantValue
        | HasIdentifier[OtherIdentifierT_co]
        | Operation[OtherIdentifierT_co],
        /,
    ) -> RelationalCondition[
        _UnconditionalVariableOperand[IdentifierT_co],
        Literal["LT"],
        Constant | OtherIdentifierT_co | Operation[OtherIdentifierT_co],
    ]:
        return RelationalCondition(
            subject=self._operation_operand,
            operator="LT",
            target=convert_to_operand(other),
        )

    @override
    # The signature is not compatible with `object.__ne__()` on purpose.
    def __ne__(  # type: ignore[override] # pyright: ignore[reportIncompatibleMethodOverride]
        self,
        other: ConstantValue
        | HasIdentifier[OtherIdentifierT_co]
        | Operation[OtherIdentifierT_co],
        /,
    ) -> RelationalCondition[
        _UnconditionalVariableOperand[IdentifierT_co],
        Literal["NE"],
        Constant | OtherIdentifierT_co | Operation[OtherIdentifierT_co],
    ]:
        assert other is not None, "Use `~isnull()` instead."
        return RelationalCondition(
            subject=self._operation_operand,
            operator="NE",
            target=convert_to_operand(other),
        )

    @final
    def __add__(
        self,
        other: ConstantValue
        | HasIdentifier[OtherIdentifierT_co]
        | Operation[OtherIdentifierT_co],
        /,
    ) -> Operation[IdentifierT_co | OtherIdentifierT_co]:
        return ArithmeticOperation(
            (self._operation_operand, convert_to_operand(other)),
            "add",
        )

    @final
    def __radd__(
        self,
        other: ConstantValue
        | HasIdentifier[OtherIdentifierT_co]
        | Operation[OtherIdentifierT_co],
        /,
    ) -> Operation[IdentifierT_co | OtherIdentifierT_co]:
        return ArithmeticOperation(
            (convert_to_operand(other), self._operation_operand),
            "add",
        )

    @final
    def __floordiv__(
        self,
        other: ConstantValue
        | HasIdentifier[OtherIdentifierT_co]
        | Operation[OtherIdentifierT_co],
        /,
    ) -> Operation[IdentifierT_co | OtherIdentifierT_co]:
        return ArithmeticOperation(
            (self._operation_operand, convert_to_operand(other)),
            "floordiv",
        )

    @final
    def __rfloordiv__(
        self,
        other: ConstantValue
        | HasIdentifier[OtherIdentifierT_co]
        | Operation[OtherIdentifierT_co],
        /,
    ) -> Operation[IdentifierT_co | OtherIdentifierT_co]:
        return ArithmeticOperation(
            (convert_to_operand(other), self._operation_operand),
            "floordiv",
        )

    @final
    def __mod__(
        self,
        other: ConstantValue
        | HasIdentifier[OtherIdentifierT_co]
        | Operation[OtherIdentifierT_co],
        /,
    ) -> Operation[IdentifierT_co | OtherIdentifierT_co]:
        return ArithmeticOperation(
            (self._operation_operand, convert_to_operand(other)),
            "mod",
        )

    @final
    def __rmod__(
        self,
        other: ConstantValue
        | HasIdentifier[OtherIdentifierT_co]
        | Operation[OtherIdentifierT_co],
        /,
    ) -> Operation[IdentifierT_co | OtherIdentifierT_co]:
        return ArithmeticOperation(
            (convert_to_operand(other), self._operation_operand),
            "mod",
        )

    @final
    def __mul__(
        self,
        other: ConstantValue
        | HasIdentifier[OtherIdentifierT_co]
        | Operation[OtherIdentifierT_co],
        /,
    ) -> Operation[IdentifierT_co | OtherIdentifierT_co]:
        return ArithmeticOperation(
            (self._operation_operand, convert_to_operand(other)),
            "mul",
        )

    @final
    def __rmul__(
        self,
        other: ConstantValue
        | HasIdentifier[OtherIdentifierT_co]
        | Operation[OtherIdentifierT_co],
        /,
    ) -> Operation[IdentifierT_co | OtherIdentifierT_co]:
        return ArithmeticOperation(
            (convert_to_operand(other), self._operation_operand),
            "mul",
        )

    @final
    def __neg__(
        self,
    ) -> Operation[IdentifierT_co]:
        return ArithmeticOperation((self._operation_operand,), "neg")

    @final
    def __pow__(
        self,
        other: ConstantValue
        | HasIdentifier[OtherIdentifierT_co]
        | Operation[OtherIdentifierT_co],
        /,
    ) -> Operation[IdentifierT_co | OtherIdentifierT_co]:
        return ArithmeticOperation(
            (self._operation_operand, convert_to_operand(other)),
            "pow",
        )

    @final
    def __rpow__(
        self,
        other: ConstantValue
        | HasIdentifier[OtherIdentifierT_co]
        | Operation[OtherIdentifierT_co],
        /,
    ) -> Operation[IdentifierT_co | OtherIdentifierT_co]:
        return ArithmeticOperation(
            (convert_to_operand(other), self._operation_operand),
            "pow",
        )

    @final
    def __sub__(
        self,
        other: ConstantValue
        | HasIdentifier[OtherIdentifierT_co]
        | Operation[OtherIdentifierT_co],
        /,
    ) -> Operation[IdentifierT_co | OtherIdentifierT_co]:
        return ArithmeticOperation(
            (self._operation_operand, convert_to_operand(other)),
            "sub",
        )

    @final
    def __rsub__(
        self,
        other: ConstantValue
        | HasIdentifier[OtherIdentifierT_co]
        | Operation[OtherIdentifierT_co],
        /,
    ) -> Operation[IdentifierT_co | OtherIdentifierT_co]:
        return ArithmeticOperation(
            (convert_to_operand(other), self._operation_operand),
            "sub",
        )

    @final
    def __truediv__(
        self,
        other: ConstantValue
        | HasIdentifier[OtherIdentifierT_co]
        | Operation[OtherIdentifierT_co],
        /,
    ) -> Operation[IdentifierT_co | OtherIdentifierT_co]:
        return ArithmeticOperation(
            (self._operation_operand, convert_to_operand(other)),
            "truediv",
        )

    @final
    def __rtruediv__(
        self,
        other: ConstantValue
        | HasIdentifier[OtherIdentifierT_co]
        | Operation[OtherIdentifierT_co],
        /,
    ) -> Operation[IdentifierT_co | OtherIdentifierT_co]:
        return ArithmeticOperation(
            (convert_to_operand(other), self._operation_operand),
            "truediv",
        )


OperandConvertibleBound = OperandConvertible[Identifier]


class _BaseOperation(ABC):
    """An operation is made out of one or more operands and possibly some other primitive attributes such as strings or numbers.

    To ensure that operations are immutable and serializable, operands must never be of type `ConstantValue` or `HasIdentifier`.
    These must be converted to `Constant` and `Identifier` instead.

    This base class' sole purpose is to provide a shared fundation for `Condition` and `Operation`.
    All classes inheriting from `_BaseOperation` must inherit from one of these two classes.
    As such, this class must remain private and not referenced outside this file.
    """

    @property
    @abstractmethod
    def _identifier_types(self) -> frozenset[type[Identifier]]:
        """The set of types of the identifiers used in this operation.

        This is used, for instance, to detect whether an operation is purely column-based and could thus be the input of a UDAF.
        """

    @classmethod
    def _get_identifier_types(
        cls,
        operand: Operand[Identifier] | None,
        /,
    ) -> frozenset[type[Identifier]]:
        if operand is None or isinstance(operand, Constant):
            return frozenset()
        if isinstance(operand, Identifier):
            return frozenset([type(operand)])
        return operand._identifier_types


class Operation(OperandConvertible[IdentifierT_co], _BaseOperation, ABC):
    @property
    @override
    def _operation_operand(self) -> Operation[IdentifierT_co]:
        return self


OperationBound = Operation[Identifier]

# The following classes can be constructed from any `OperandConvertible` using Python's built-in operators.
# Because overriding these operators requires to implement methods on `OperandConvertible` instantiating the classes below, they all have to be declared in the same file to avoid circular imports.


# Using `BaseModel` instead of `dataclass` because Pydantic does not support validation of generic dataclass attributes.
# See https://github.com/pydantic/pydantic/issues/5803.
# Do not make this class and the ones inheriting from it public until this is fixed because `BaseModel` classes have many methods such as `dump_json()` that should not be part of Atoti's public API.
class BaseCondition(
    BaseModel, _BaseOperation, arbitrary_types_allowed=True, frozen=True
):
    @overload
    def __and__(  # type: ignore[misc]
        self: LogicalConditionLeafOperandT_co,
        other: OtherLogicalConditionLeafOperandT,
        /,
    ) -> LogicalCondition[
        LogicalConditionLeafOperandT_co | OtherLogicalConditionLeafOperandT,
        Literal["AND"],
    ]: ...

    @overload
    def __and__(  #  type: ignore[misc]
        self: LogicalConditionLeafOperandT_co,
        other: LogicalCondition[
            OtherLogicalConditionLeafOperandT, OtherLogicalConditionOperatorT
        ],
        /,
    ) -> LogicalCondition[
        LogicalConditionLeafOperandT_co | OtherLogicalConditionLeafOperandT,
        Literal["AND"] | OtherLogicalConditionOperatorT,
    ]: ...

    @overload
    def __and__(  #  type: ignore[misc]
        self: LogicalCondition[
            LogicalConditionLeafOperandT_co, LogicalConditionOperatorT_co
        ],
        other: OtherLogicalConditionLeafOperandT,
        /,
    ) -> LogicalCondition[
        LogicalConditionLeafOperandT_co | OtherLogicalConditionLeafOperandT,
        Literal["AND"] | LogicalConditionOperatorT_co,
    ]: ...

    @overload
    def __and__(  #  type: ignore[misc]
        self: LogicalCondition[
            LogicalConditionLeafOperandT_co, LogicalConditionOperatorT_co
        ],
        other: LogicalCondition[
            OtherLogicalConditionLeafOperandT, OtherLogicalConditionOperatorT
        ],
        /,
    ) -> LogicalCondition[
        LogicalConditionLeafOperandT_co | OtherLogicalConditionLeafOperandT,
        Literal["AND"] | LogicalConditionOperatorT_co | OtherLogicalConditionOperatorT,
    ]: ...

    def __and__(
        self,
        other: ConditionBound,
        /,
    ) -> LogicalConditionBound:
        assert isinstance(self, Condition)
        return LogicalCondition(operands=(self, other), operator="AND")

    @final
    def __bool__(self) -> NoReturn:
        raise RuntimeError(
            "Conditions cannot be cast to a boolean since they are only evaluated during query execution. To combine conditions, use the bitwise `&`, `|`, or `~` operators.",
        )

    @abstractmethod
    def __invert__(self) -> ConditionBound: ...

    @overload
    def __or__(  #  type: ignore[misc]
        self: LogicalConditionLeafOperandT_co,
        other: OtherLogicalConditionLeafOperandT,
        /,
    ) -> LogicalCondition[
        LogicalConditionLeafOperandT_co | OtherLogicalConditionLeafOperandT,
        Literal["OR"],
    ]: ...

    @overload
    def __or__(  #  type: ignore[misc]
        self: LogicalConditionLeafOperandT_co,
        other: LogicalCondition[
            OtherLogicalConditionLeafOperandT, OtherLogicalConditionOperatorT
        ],
        /,
    ) -> LogicalCondition[
        LogicalConditionLeafOperandT_co | OtherLogicalConditionLeafOperandT,
        Literal["OR"] | OtherLogicalConditionOperatorT,
    ]: ...

    @overload
    def __or__(  #  type: ignore[misc]
        self: LogicalCondition[
            LogicalConditionLeafOperandT_co, LogicalConditionOperatorT_co
        ],
        other: OtherLogicalConditionLeafOperandT,
        /,
    ) -> LogicalCondition[
        LogicalConditionLeafOperandT_co | OtherLogicalConditionLeafOperandT,
        Literal["OR"] | LogicalConditionOperatorT_co,
    ]: ...

    @overload
    def __or__(  #  type: ignore[misc]
        self: LogicalCondition[
            LogicalConditionLeafOperandT_co, LogicalConditionOperatorT_co
        ],
        other: LogicalCondition[
            OtherLogicalConditionLeafOperandT, OtherLogicalConditionOperatorT
        ],
        /,
    ) -> LogicalCondition[
        LogicalConditionLeafOperandT_co | OtherLogicalConditionLeafOperandT,
        Literal["OR"] | LogicalConditionOperatorT_co | OtherLogicalConditionOperatorT,
    ]: ...

    def __or__(
        self,
        other: ConditionBound,
        /,
    ) -> LogicalConditionBound:
        assert isinstance(self, Condition)
        return LogicalCondition(operands=(self, other), operator="OR")

    @override
    def __str__(self) -> str:
        return repr(self)

    @final
    def __xor__(self, other: ConditionBound, /) -> NoReturn:
        raise RuntimeError(
            "Conditions cannot be `xor`ed.",
        )


HierarchyIsInContionOperatorBound = IsInOperator
HierarchyIsInContionOperatorT_co = TypeVar(
    "HierarchyIsInContionOperatorT_co",
    bound=IsInOperator,
    covariant=True,
)


def _validate_constant_target(target: Constant, /) -> Constant:
    if isinstance(target.value, float) and math.isnan(target.value):
        raise ValueError("Use the `isnan()` method to compare against NaN.")

    return target


@final
class HierarchyIsInCondition(
    BaseCondition, Generic[HierarchyIsInContionOperatorT_co], frozen=True
):
    subject: HierarchyIdentifier
    operator: HierarchyIsInContionOperatorT_co
    member_paths: Annotated[
        AbstractSet[
            Annotated[
                tuple[
                    Annotated[Constant, AfterValidator(_validate_constant_target)],
                    ...,
                ],
                Field(min_length=1),
            ]
        ],
        Field(min_length=1),
    ]
    level_names: Annotated[FrozenSequence[LevelName], Field(min_length=1, repr=False)]

    @property
    @override
    def _identifier_types(self) -> frozenset[type[Identifier]]:
        return frozenset({HierarchyIdentifier})

    # Not a `@property` to be able to use `@overload`
    @overload
    def _logical_relational(
        self: HierarchyIsInCondition[Literal["IS_IN"]], /
    ) -> (
        RelationalCondition[LevelIdentifier, Literal["EQ"], Constant | None]
        | LogicalCondition[
            RelationalCondition[LevelIdentifier, Literal["EQ"], Constant | None],
            LogicalConditionOperatorBound,
        ]
    ): ...

    @overload
    def _logical_relational(
        self: HierarchyIsInCondition[Literal["IS_NOT_IN"]], /
    ) -> (
        RelationalCondition[LevelIdentifier, Literal["NE"], Constant | None]
        | LogicalCondition[
            RelationalCondition[LevelIdentifier, Literal["NE"], Constant | None],
            LogicalConditionOperatorBound,
        ]
    ): ...

    @overload
    def _logical_relational(
        self, /
    ) -> (
        RelationalCondition[LevelIdentifier, Literal["EQ", "NE"], Constant | None]
        | LogicalCondition[
            RelationalCondition[LevelIdentifier, Literal["EQ", "NE"], Constant | None],
            LogicalConditionOperatorBound,
        ]
    ): ...

    def _logical_relational(
        self, /
    ) -> (
        RelationalCondition[LevelIdentifier, Literal["EQ", "NE"], Constant | None]
        | LogicalCondition[
            RelationalCondition[LevelIdentifier, Literal["EQ", "NE"], Constant | None],
            LogicalConditionOperatorBound,
        ]
    ):
        from .condition_from_disjunctive_normal_form import (  # pylint: disable=nested-import
            condition_from_disjunctive_normal_form,
        )

        match self.operator:
            case "IS_IN":
                return condition_from_disjunctive_normal_form(
                    [
                        [
                            RelationalCondition(
                                subject=LevelIdentifier(self.subject, level_name),
                                operator="EQ",
                                target=value,
                            )
                            for value, level_name in zip(
                                member_path, self.level_names, strict=False
                            )
                        ]
                        for member_path in sorted(self.member_paths)
                    ]
                )
            case "IS_NOT_IN":
                return cast(
                    RelationalCondition[
                        LevelIdentifier, Literal["EQ", "NE"], Constant | None
                    ]
                    | LogicalCondition[
                        RelationalCondition[
                            LevelIdentifier, Literal["EQ", "NE"], Constant | None
                        ],
                        LogicalConditionOperatorBound,
                    ],
                    ~((~self)._logical_relational()),
                )

    @overload
    def __invert__(
        self: HierarchyIsInCondition[Literal["IS_IN"]], /
    ) -> HierarchyIsInCondition[Literal["IS_NOT_IN"]]: ...

    @overload
    def __invert__(
        self: HierarchyIsInCondition[Literal["IS_NOT_IN"]], /
    ) -> HierarchyIsInCondition[Literal["IS_IN"]]: ...

    @overload
    def __invert__(self, /) -> HierarchyIsInConditionBound: ...

    @override
    def __invert__(self, /) -> HierarchyIsInConditionBound:
        return HierarchyIsInCondition(
            subject=self.subject,
            operator=INVERSE_IS_IN_OPERATOR[self.operator],
            member_paths=self.member_paths,
            level_names=self.level_names,
        )

    @override
    def __repr__(self) -> str:
        match self.operator:
            case "IS_IN":
                operator = ""
            case "IS_NOT_IN":
                operator = "~"

        return f"{operator}{self.subject}.isin{tuple(tuple(member.value for member in member_path) for member_path in sorted(self.member_paths))}"


HierarchyIsInConditionBound = HierarchyIsInCondition[HierarchyIsInContionOperatorBound]


IsInConditionSubjectBound = Identifier
IsInConditionSubjectT_co = TypeVar(
    "IsInConditionSubjectT_co",
    bound=IsInConditionSubjectBound,
    covariant=True,
)

IsInConditionOperatorBound = IsInOperator
IsInConditionOperatorT_co = TypeVar(
    "IsInConditionOperatorT_co",
    bound=IsInConditionOperatorBound,
    covariant=True,
)

IsInConditionElementBound = Constant | None
IsInConditionElementT_co = TypeVar(
    "IsInConditionElementT_co",
    bound=IsInConditionElementBound,
    covariant=True,
)


def _validate_is_in_condition_subject(
    subject: IsInConditionSubjectT_co,  # type: ignore[misc]
    /,
) -> IsInConditionSubjectT_co:
    assert not isinstance(
        subject,
        HierarchyIdentifier,
    ), f"Conditions on hierarchies must use `{HierarchyIsInCondition.__name__}`."
    return subject


def _validate_element(
    element: IsInConditionElementT_co,  # type: ignore[misc]
    /,
) -> IsInConditionElementT_co:
    return (
        element  # type: ignore[return-value]
        if element is None
        else _validate_constant_target(element)
    )


@final
class IsInCondition(
    BaseCondition,
    Generic[
        IsInConditionSubjectT_co,
        IsInConditionOperatorT_co,
        IsInConditionElementT_co,
    ],
    frozen=True,
):
    subject: Annotated[
        IsInConditionSubjectT_co, AfterValidator(_validate_is_in_condition_subject)
    ]
    operator: IsInConditionOperatorT_co
    elements: Annotated[
        AbstractSet[
            Annotated[IsInConditionElementT_co, AfterValidator(_validate_element)]
        ],
        Field(min_length=2),
    ]

    @overload
    @classmethod
    def of(
        cls,
        *,
        subject: IsInConditionSubjectT_co,  # type: ignore[misc] # pyright: ignore[reportGeneralTypeIssues]
        operator: Literal["IS_IN"],
        elements: AbstractSet[IsInConditionElementT_co],
    ) -> (
        IsInCondition[
            IsInConditionSubjectT_co, Literal["IS_IN"], IsInConditionElementT_co
        ]
        | RelationalCondition[
            IsInConditionSubjectT_co, Literal["EQ"], IsInConditionElementT_co
        ]
    ): ...

    @overload
    @classmethod
    def of(
        cls,
        *,
        subject: IsInConditionSubjectT_co,  # type: ignore[misc] # pyright: ignore[reportGeneralTypeIssues]
        operator: Literal["IS_NOT_IN"],
        elements: AbstractSet[IsInConditionElementT_co],
    ) -> (
        IsInCondition[
            IsInConditionSubjectT_co, Literal["IS_NOT_IN"], IsInConditionElementT_co
        ]
        | RelationalCondition[
            IsInConditionSubjectT_co, Literal["NE"], IsInConditionElementT_co
        ]
    ): ...

    @overload
    @classmethod
    def of(
        cls,
        *,
        subject: IsInConditionSubjectT_co,  # type: ignore[misc] # pyright: ignore[reportGeneralTypeIssues]
        operator: IsInConditionOperatorT_co,  # type: ignore[misc] # pyright: ignore[reportGeneralTypeIssues]
        elements: AbstractSet[IsInConditionElementT_co],
    ) -> (
        IsInCondition[
            IsInConditionSubjectT_co,
            IsInConditionOperatorT_co,
            IsInConditionElementT_co,
        ]
        | RelationalCondition[
            IsInConditionSubjectT_co, Literal["EQ", "NE"], IsInConditionElementT_co
        ]
    ): ...

    @classmethod  # type: ignore[misc]
    def of(  # pyright: ignore[reportInconsistentOverload]
        cls,
        *,
        subject: IsInConditionSubjectT_co,  # type: ignore[misc] # pyright: ignore[reportGeneralTypeIssues]
        operator: IsInConditionOperatorT_co,  # type: ignore[misc] # pyright: ignore[reportGeneralTypeIssues]
        elements: AbstractSet[IsInConditionElementT_co],
    ) -> (
        IsInCondition[
            IsInConditionSubjectT_co,
            IsInConditionOperatorT_co,
            IsInConditionElementT_co,
        ]
        | RelationalCondition[
            IsInConditionSubjectT_co, Literal["EQ", "NE"], IsInConditionElementT_co
        ]
    ):
        if len(elements) == 1:
            return RelationalCondition(
                subject=subject,
                operator="EQ" if operator == "IS_IN" else "NE",
                target=next(iter(elements)),
            )

        return cls(subject=subject, operator=operator, elements=elements)

    @property
    @override
    def _identifier_types(self) -> frozenset[type[Identifier]]:
        return frozenset({type(self.subject)})

    # Not a `@property` to be able to use `@overload`
    @overload
    def _logical_relational(
        self: IsInCondition[
            IsInConditionSubjectT_co, Literal["IS_IN"], IsInConditionElementT_co
        ],
        /,
    ) -> (
        RelationalCondition[
            IsInConditionSubjectT_co, Literal["EQ"], IsInConditionElementT_co
        ]
        | LogicalCondition[
            RelationalCondition[
                IsInConditionSubjectT_co, Literal["EQ"], IsInConditionElementT_co
            ],
            Literal["OR"],
        ]
    ): ...

    @overload
    def _logical_relational(
        self: IsInCondition[
            IsInConditionSubjectT_co, Literal["IS_NOT_IN"], IsInConditionElementT_co
        ],
        /,
    ) -> (
        RelationalCondition[
            IsInConditionSubjectT_co, Literal["NE"], IsInConditionElementT_co
        ]
        | LogicalCondition[
            RelationalCondition[
                IsInConditionSubjectT_co, Literal["NE"], IsInConditionElementT_co
            ],
            Literal["AND"],
        ]
    ): ...

    @overload
    def _logical_relational(
        self: IsInCondition[
            IsInConditionSubjectT_co,
            IsInConditionOperatorBound,
            IsInConditionElementT_co,
        ],
        /,
    ) -> (
        RelationalCondition[
            IsInConditionSubjectT_co, Literal["EQ", "NE"], IsInConditionElementT_co
        ]
        | LogicalCondition[
            RelationalCondition[
                IsInConditionSubjectT_co, Literal["EQ", "NE"], IsInConditionElementT_co
            ],
            LogicalConditionOperatorBound,
        ]
    ): ...

    def _logical_relational(
        self: IsInCondition[
            IsInConditionSubjectT_co,
            IsInConditionOperatorBound,
            IsInConditionElementT_co,
        ],
        /,
    ) -> (
        RelationalCondition[
            IsInConditionSubjectT_co, Literal["EQ", "NE"], IsInConditionElementT_co
        ]
        | LogicalCondition[
            RelationalCondition[
                IsInConditionSubjectT_co, Literal["EQ", "NE"], IsInConditionElementT_co
            ],
            LogicalConditionOperatorBound,
        ]
    ):
        from .condition_from_disjunctive_normal_form import (  # pylint: disable=nested-import
            condition_from_disjunctive_normal_form,
        )

        match self.operator:
            case "IS_IN":
                return condition_from_disjunctive_normal_form(
                    tuple(
                        (
                            RelationalCondition(
                                subject=self.subject, operator="EQ", target=element
                            ),
                        )
                        for element in self._sorted_elements
                    )
                )
            case "IS_NOT_IN":
                return cast(
                    RelationalCondition[
                        IsInConditionSubjectT_co,
                        Literal["EQ", "NE"],
                        IsInConditionElementT_co,
                    ]
                    | LogicalCondition[
                        RelationalCondition[
                            IsInConditionSubjectT_co,
                            Literal["EQ", "NE"],
                            IsInConditionElementT_co,
                        ],
                        LogicalConditionOperatorBound,
                    ],
                    ~((~self)._logical_relational()),
                )

    @property
    def _sorted_elements(self) -> tuple[IsInConditionElementT_co, ...]:
        return (
            # Collections containing `None` cannot be sorted.
            # If `None` is in the elements it's added at the head of the tuple.
            # The remaining non-`None` elements are sorted and inserted after.
            *([None] if None in self.elements else []),  # type: ignore[arg-type] # pyright: ignore[reportReturnType]
            *sorted(element for element in self.elements if element is not None),
        )

    @overload
    def __invert__(
        self: IsInCondition[
            IsInConditionSubjectT_co, Literal["IS_IN"], IsInConditionElementT_co
        ],
        /,
    ) -> IsInCondition[
        IsInConditionSubjectT_co, Literal["IS_NOT_IN"], IsInConditionElementT_co
    ]: ...

    @overload
    def __invert__(
        self: IsInCondition[
            IsInConditionSubjectT_co, Literal["IS_NOT_IN"], IsInConditionElementT_co
        ],
        /,
    ) -> IsInCondition[
        IsInConditionSubjectT_co, Literal["IS_IN"], IsInConditionElementT_co
    ]: ...

    @overload
    def __invert__(
        self: IsInCondition[
            IsInConditionSubjectT_co,
            IsInConditionOperatorBound,
            IsInConditionElementT_co,
        ],
        /,
    ) -> IsInCondition[
        IsInConditionSubjectT_co, IsInConditionOperatorBound, IsInConditionElementT_co
    ]: ...

    @override
    def __invert__(self, /) -> IsInConditionBound:
        return IsInCondition(
            subject=self.subject,
            operator=INVERSE_IS_IN_OPERATOR[self.operator],
            elements=self.elements,
        )

    @override
    def __repr__(self) -> str:
        match self.operator:
            case "IS_IN":
                operator = ""
            case "IS_NOT_IN":
                operator = "~"

        return f"{operator}{self.subject}.isin{tuple(element.value if isinstance(element, Constant) else element for element in self._sorted_elements)}"


IsInConditionBound = IsInCondition[
    IsInConditionSubjectBound, IsInConditionOperatorBound, IsInConditionElementBound
]

RelationalConditionSubjectBound = Identifier | OperationBound
RelationalConditionSubjectT_co = TypeVar(
    "RelationalConditionSubjectT_co",
    bound=RelationalConditionSubjectBound,
    covariant=True,
)

RelationalConditionOperatorBound = RelationalOperator
RelationalConditionOperatorT_co = TypeVar(
    "RelationalConditionOperatorT_co",
    bound=RelationalOperator,
    covariant=True,
)

RelationalConditionTargetBound = Constant | Identifier | OperationBound | None
RelationalConditionTargetT_co = TypeVar(
    "RelationalConditionTargetT_co",
    bound=RelationalConditionTargetBound,
    covariant=True,
)


def _validate_relational_condition_subject(
    subject: RelationalConditionSubjectT_co,  # type: ignore[misc]
    /,
) -> RelationalConditionSubjectT_co:
    assert not isinstance(
        subject,
        HierarchyIdentifier,
    ), f"Conditions on hierarchies must use `{HierarchyIsInCondition.__name__}`."
    return subject


def _validate_relational_condition_target(
    target: RelationalConditionTargetT_co,  # type: ignore[misc]
    /,
) -> RelationalConditionTargetT_co:
    return _validate_constant_target(target) if isinstance(target, Constant) else target  # type: ignore[return-value]


_SYMBOL_FROM_RELATIONAL_OPERATOR: Mapping[RelationalOperator, str] = {
    "EQ": "==",
    "GE": ">=",
    "GT": ">",
    "LE": "<=",
    "LT": "<",
    "NE": "!=",
}


@final
class RelationalCondition(
    BaseCondition,
    Generic[
        RelationalConditionSubjectT_co,
        RelationalConditionOperatorT_co,
        RelationalConditionTargetT_co,
    ],
    frozen=True,
):
    subject: Annotated[
        RelationalConditionSubjectT_co,
        AfterValidator(_validate_relational_condition_subject),
    ]
    operator: RelationalConditionOperatorT_co
    target: Annotated[
        RelationalConditionTargetT_co,
        AfterValidator(_validate_relational_condition_target),
    ]

    def __post_init__(self) -> None:
        if self.target is None and self.operator not in {"EQ", "NE"}:
            raise ValueError(
                f"`{self.target}` target cannot be used with `{self.operator}` operator."
            )

    @property
    @override
    def _identifier_types(self) -> frozenset[type[Identifier]]:
        return frozenset(
            chain(
                *(
                    self._get_identifier_types(operand)
                    for operand in [self.subject, self.target]
                ),
            ),
        )

    @overload
    def __invert__(
        self: RelationalCondition[
            RelationalConditionSubjectT_co, Literal["EQ"], RelationalConditionTargetT_co
        ],
        /,
    ) -> RelationalCondition[
        RelationalConditionSubjectT_co, Literal["NE"], RelationalConditionTargetT_co
    ]: ...

    @overload
    def __invert__(
        self: RelationalCondition[
            RelationalConditionSubjectT_co, Literal["GE"], RelationalConditionTargetT_co
        ],
        /,
    ) -> RelationalCondition[
        RelationalConditionSubjectT_co, Literal["LT"], RelationalConditionTargetT_co
    ]: ...

    @overload
    def __invert__(
        self: RelationalCondition[
            RelationalConditionSubjectT_co, Literal["GT"], RelationalConditionTargetT_co
        ],
        /,
    ) -> RelationalCondition[
        RelationalConditionSubjectT_co, Literal["LE"], RelationalConditionTargetT_co
    ]: ...

    @overload
    def __invert__(
        self: RelationalCondition[
            RelationalConditionSubjectT_co, Literal["LE"], RelationalConditionTargetT_co
        ],
        /,
    ) -> RelationalCondition[
        RelationalConditionSubjectT_co, Literal["GT"], RelationalConditionTargetT_co
    ]: ...

    @overload
    def __invert__(
        self: RelationalCondition[
            RelationalConditionSubjectT_co, Literal["LT"], RelationalConditionTargetT_co
        ],
        /,
    ) -> RelationalCondition[
        RelationalConditionSubjectT_co, Literal["GE"], RelationalConditionTargetT_co
    ]: ...

    @overload
    def __invert__(
        self: RelationalCondition[
            RelationalConditionSubjectT_co, Literal["NE"], RelationalConditionTargetT_co
        ],
        /,
    ) -> RelationalCondition[
        RelationalConditionSubjectT_co, Literal["EQ"], RelationalConditionTargetT_co
    ]: ...

    @overload
    def __invert__(
        self: RelationalCondition[
            RelationalConditionSubjectT_co,
            RelationalConditionOperatorBound,
            RelationalConditionTargetT_co,
        ],
        /,
    ) -> RelationalCondition[
        RelationalConditionSubjectT_co,
        RelationalConditionOperatorBound,
        RelationalConditionTargetT_co,
    ]: ...

    @override
    def __invert__(self, /) -> RelationalConditionBound:
        return RelationalCondition(
            subject=self.subject,
            operator=INVERSE_RELATIONAL_OPERATOR[self.operator],
            target=self.target,
        )

    @override
    def __repr__(self) -> str:
        if self.target is None:
            assert self.operator == "EQ" or self.operator == "NE"
            return f"{'' if self.operator == 'EQ' else '~'}{self.subject}.isnull()"

        return f"{self.subject} {_SYMBOL_FROM_RELATIONAL_OPERATOR[self.operator]} {self.target.value if isinstance(self.target, Constant) else self.target!r}"


RelationalConditionBound = RelationalCondition[
    RelationalConditionSubjectBound,
    RelationalConditionOperatorBound,
    RelationalConditionTargetBound,
]

LogicalConditionLeafOperandBound = (
    HierarchyIsInConditionBound | IsInConditionBound | RelationalConditionBound
)
LogicalConditionLeafOperandT_co = TypeVar(
    "LogicalConditionLeafOperandT_co",
    bound=LogicalConditionLeafOperandBound,
    covariant=True,
)

LogicalConditionOperatorBound = LogicalOperator
LogicalConditionOperatorT_co = TypeVar(
    "LogicalConditionOperatorT_co",
    bound=LogicalConditionOperatorBound,
    covariant=True,
)

_SYMBOL_FROM_LOGICAL_OPERATOR: Mapping[LogicalConditionOperatorBound, str] = {
    "AND": "&",
    "OR": "|",
}


@final
class LogicalCondition(
    BaseCondition,
    Generic[
        LogicalConditionLeafOperandT_co,
        LogicalConditionOperatorT_co,
    ],
    frozen=True,
):
    # See https://github.com/pydantic/pydantic/issues/7905#issuecomment-1783302168.
    operands: SerializeAsAny[
        tuple[
            LogicalConditionLeafOperandT_co
            | LogicalCondition[
                LogicalConditionLeafOperandT_co, LogicalConditionOperatorT_co
            ],
            LogicalConditionLeafOperandT_co
            | LogicalCondition[
                LogicalConditionLeafOperandT_co, LogicalConditionOperatorT_co
            ],
        ]
    ]
    operator: LogicalConditionOperatorT_co

    @property
    @override
    def _identifier_types(self) -> frozenset[type[Identifier]]:
        return frozenset(
            chain(
                *(operand._identifier_types for operand in self.operands),
            ),
        )

    @overload
    def __invert__(
        self: LogicalCondition[
            HierarchyIsInConditionBound,
            LogicalConditionOperatorBound,
        ],
        /,
    ) -> LogicalCondition[
        HierarchyIsInConditionBound,
        LogicalConditionOperatorBound,
    ]: ...

    @overload
    def __invert__(
        self: LogicalCondition[
            IsInCondition[
                IsInConditionSubjectT_co,
                IsInConditionOperatorBound,
                IsInConditionElementT_co,
            ],
            LogicalConditionOperatorBound,
        ],
        /,
    ) -> LogicalCondition[
        IsInCondition[
            IsInConditionSubjectT_co,
            IsInConditionOperatorBound,
            IsInConditionElementT_co,
        ],
        LogicalConditionOperatorBound,
    ]: ...

    @overload
    def __invert__(  # type: ignore[overload-overlap] # pyright: ignore[reportOverlappingOverload]
        self: LogicalCondition[
            HierarchyIsInConditionBound
            | IsInCondition[
                IsInConditionSubjectT_co,
                IsInConditionOperatorBound,
                IsInConditionElementT_co,
            ],
            LogicalConditionOperatorBound,
        ],
        /,
    ) -> LogicalCondition[
        HierarchyIsInConditionBound
        | IsInCondition[
            IsInConditionSubjectT_co,
            IsInConditionOperatorBound,
            IsInConditionElementT_co,
        ],
        LogicalConditionOperatorBound,
    ]: ...

    @overload
    def __invert__(
        self: LogicalCondition[
            RelationalCondition[
                RelationalConditionSubjectT_co,
                RelationalConditionOperatorBound,
                RelationalConditionTargetT_co,
            ],
            LogicalConditionOperatorBound,
        ],
        /,
    ) -> LogicalCondition[
        RelationalCondition[
            RelationalConditionSubjectT_co,
            RelationalConditionOperatorBound,
            RelationalConditionTargetT_co,
        ],
        LogicalConditionOperatorBound,
    ]: ...

    @overload
    def __invert__(  # type: ignore[overload-overlap]
        self: LogicalCondition[
            HierarchyIsInConditionBound
            | RelationalCondition[
                RelationalConditionSubjectT_co,
                RelationalConditionOperatorBound,
                RelationalConditionTargetT_co,
            ],
            LogicalConditionOperatorBound,
        ],
        /,
    ) -> LogicalCondition[
        HierarchyIsInConditionBound
        | RelationalCondition[
            RelationalConditionSubjectT_co,
            RelationalConditionOperatorBound,
            RelationalConditionTargetT_co,
        ],
        LogicalConditionOperatorBound,
    ]: ...

    @overload
    def __invert__(
        self: LogicalCondition[
            IsInCondition[
                IsInConditionSubjectT_co,
                IsInConditionOperatorBound,
                IsInConditionElementT_co,
            ]
            | RelationalCondition[
                RelationalConditionSubjectT_co,
                RelationalConditionOperatorBound,
                RelationalConditionTargetT_co,
            ],
            LogicalConditionOperatorBound,
        ],
        /,
    ) -> LogicalCondition[
        IsInCondition[
            IsInConditionSubjectT_co,
            IsInConditionOperatorBound,
            IsInConditionElementT_co,
        ]
        | RelationalCondition[
            RelationalConditionSubjectT_co,
            RelationalConditionOperatorBound,
            RelationalConditionTargetT_co,
        ],
        LogicalConditionOperatorBound,
    ]: ...

    @overload
    def __invert__(
        self: LogicalCondition[
            HierarchyIsInConditionBound
            | IsInCondition[
                IsInConditionSubjectT_co,
                IsInConditionOperatorBound,
                IsInConditionElementT_co,
            ]
            | RelationalCondition[
                RelationalConditionSubjectT_co,
                RelationalConditionOperatorBound,
                RelationalConditionTargetT_co,
            ],
            LogicalConditionOperatorBound,
        ],
        /,
    ) -> LogicalCondition[
        HierarchyIsInConditionBound
        | IsInCondition[
            IsInConditionSubjectT_co,
            IsInConditionOperatorBound,
            IsInConditionElementT_co,
        ]
        | RelationalCondition[
            RelationalConditionSubjectT_co,
            RelationalConditionOperatorBound,
            RelationalConditionTargetT_co,
        ],
        LogicalConditionOperatorBound,
    ]: ...

    @override
    def __invert__(self, /) -> LogicalConditionBound:
        return LogicalCondition(
            operands=(~self.operands[0], ~self.operands[1]),
            operator="OR" if self.operator == "AND" else "AND",
        )

    @override
    def __repr__(self) -> str:
        def _repr_operand(operand: ConditionBound, /) -> str:
            match operand:
                case LogicalCondition():
                    return (
                        str(operand)
                        if operand.operator == self.operator
                        else f"({operand})"
                    )
                case RelationalCondition():
                    return str(operand) if operand.target is None else f"({operand})"
                case HierarchyIsInCondition() | IsInCondition():
                    return str(operand)

        left, right = self.operands
        return f"{_repr_operand(left)} {_SYMBOL_FROM_LOGICAL_OPERATOR[self.operator]} {_repr_operand(right)}"


LogicalConditionBound = LogicalCondition[
    LogicalConditionLeafOperandBound, LogicalConditionOperatorBound
]


Condition = (
    HierarchyIsInCondition | IsInCondition | LogicalCondition | RelationalCondition  # type: ignore[type-arg] # pyright: ignore[reportMissingTypeArgument]
)
ConditionBound = LogicalConditionLeafOperandBound | LogicalConditionBound


OtherLogicalConditionLeafOperandT = TypeVar(
    "OtherLogicalConditionLeafOperandT",
    bound=LogicalConditionLeafOperandBound,
)
OtherLogicalConditionOperatorT = TypeVar(
    "OtherLogicalConditionOperatorT",
    bound=LogicalConditionOperatorBound,
)

_SYMBOL_FROM_ARITHMETIC_OPERATOR: Mapping[ArithmeticOperator, str] = {
    "add": "+",
    "floordiv": "//",
    "mod": "%",
    "mul": "*",
    "pow": "**",
    "sub": "-",
    "truediv": "/",
}


@final
@dataclass(config=_PYDANTIC_CONFIG, eq=False, frozen=True)
class ArithmeticOperation(Operation[IdentifierT_co]):
    operands: FrozenSequence[_UnconditionalOperand[IdentifierT_co]]
    operator: ArithmeticOperator
    _: KW_ONLY

    @property
    @override
    def _identifier_types(self) -> frozenset[type[Identifier]]:
        return frozenset(
            chain(*(self._get_identifier_types(operand) for operand in self.operands)),
        )

    @override
    def __repr__(self) -> str:
        if self.operator == "neg":
            return f"-{self._repr_operand(0)}"

        return f"{self._repr_operand(0)} {_SYMBOL_FROM_ARITHMETIC_OPERATOR[self.operator]} {self._repr_operand(1)}"

    def _repr_operand(self, index: int, /) -> str:
        operand = self.operands[index]
        operand_representation = repr(operand)
        operation_is_function_call_result = not isinstance(
            operand,
            ArithmeticOperation | Condition | IndexingOperation,
        )
        return (
            operand_representation
            if operation_is_function_call_result
            else f"({operand_representation})"
        )


@final
@_dataclass(eq=False, frozen=True)
class IndexingOperation(Operation[IdentifierT_co]):
    operand: _UnconditionalVariableOperand[IdentifierT_co]
    index: (
        slice | int | FrozenSequence[int] | IdentifierT_co | Operation[IdentifierT_co]
    )
    _: KW_ONLY

    @property
    @override
    def _identifier_types(self) -> frozenset[type[Identifier]]:
        return self._get_identifier_types(self.operand) | (
            frozenset()
            if isinstance(self.index, int | Sequence | slice)
            else self._get_identifier_types(self.index)
        )

    @override
    def __repr__(self) -> str:
        return f"{self.operand}[{self.index}]"


_UnconditionalVariableOperand: TypeAlias = IdentifierT_co | Operation[IdentifierT_co]
_UnconditionalOperand: TypeAlias = (
    Constant | _UnconditionalVariableOperand[IdentifierT_co]
)


_OperandLeafCondition: TypeAlias = RelationalCondition[
    _UnconditionalVariableOperand[IdentifierT_co],
    RelationalConditionOperatorBound,
    _UnconditionalOperand[IdentifierT_co] | None,
]
_OperandLeafCondition.__parameters__ = (IdentifierT_co,)  # type: ignore[attr-defined] # pyright: ignore[reportAttributeAccessIssue]
_OperandLogicalCondition: TypeAlias = LogicalCondition[
    _OperandLeafCondition[IdentifierT_co],
    LogicalConditionOperatorBound,
]
_OperandLogicalCondition.__parameters__ = (IdentifierT_co,)  # type: ignore[attr-defined] # pyright: ignore[reportAttributeAccessIssue]
OperandCondition: TypeAlias = Union[  # noqa: UP007
    _OperandLeafCondition[IdentifierT_co], _OperandLogicalCondition[IdentifierT_co]
]
OperandCondition.__dict__["__parameters__"] = (IdentifierT_co,)


_VariableOperand: TypeAlias = (
    _UnconditionalVariableOperand[IdentifierT_co] | OperandCondition[IdentifierT_co]
)
Operand: TypeAlias = Constant | _VariableOperand[IdentifierT_co]
