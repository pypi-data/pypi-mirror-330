from typing import Literal, cast

from .._typing import get_literal_args

LogicalOperator = Literal["AND", "OR"]


LOGICAL_OPERATORS = cast(
    tuple[LogicalOperator, ...],
    get_literal_args(LogicalOperator),
)
