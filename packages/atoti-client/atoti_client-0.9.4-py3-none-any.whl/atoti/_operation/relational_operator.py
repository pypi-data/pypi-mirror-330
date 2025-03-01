from collections.abc import Mapping
from typing import Literal, cast

RelationalOperator = Literal["EQ", "GE", "GT", "LE", "LT", "NE"]


_INVERSE_OPERATOR_ONE_WAY: Mapping[
    RelationalOperator,
    RelationalOperator,
] = {
    "EQ": "NE",
    "LT": "GE",
    "LE": "GT",
}

INVERSE_RELATIONAL_OPERATOR: Mapping[RelationalOperator, RelationalOperator] = cast(
    Mapping[RelationalOperator, RelationalOperator],
    {
        **_INVERSE_OPERATOR_ONE_WAY,
        **{value: key for key, value in _INVERSE_OPERATOR_ONE_WAY.items()},
    },
)

RELATIONAL_OPERATORS = tuple(INVERSE_RELATIONAL_OPERATOR)
