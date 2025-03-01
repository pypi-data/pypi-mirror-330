from collections.abc import Mapping
from typing import Literal, cast

IsInOperator = Literal["IS_IN", "IS_NOT_IN"]


_INVERSE_OPERATOR_ONE_WAY: Mapping[
    IsInOperator,
    IsInOperator,
] = {
    "IS_IN": "IS_NOT_IN",
}

INVERSE_IS_IN_OPERATOR: Mapping[IsInOperator, IsInOperator] = cast(
    Mapping[IsInOperator, IsInOperator],
    {
        **_INVERSE_OPERATOR_ONE_WAY,
        **{value: key for key, value in _INVERSE_OPERATOR_ONE_WAY.items()},
    },
)

IS_IN_OPERATORS = tuple(INVERSE_IS_IN_OPERATOR)
