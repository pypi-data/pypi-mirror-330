from collections.abc import Sequence
from datetime import date, datetime, time
from typing import Annotated, TypeAlias

from pydantic import Field

ConstantValue: TypeAlias = (
    bool
    | int
    | float
    | date
    | datetime
    | time
    | Annotated[Sequence[bool], Field(min_length=1)]
    | Annotated[Sequence[int], Field(min_length=1)]
    | Annotated[Sequence[float], Field(min_length=1)]
    | Annotated[Sequence[str], Field(min_length=1)]
    | str
)
