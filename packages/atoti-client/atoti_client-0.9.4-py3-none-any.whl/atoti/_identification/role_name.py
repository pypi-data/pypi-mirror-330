from typing import Annotated, TypeAlias

from pydantic import Field

RoleName: TypeAlias = Annotated[str, Field(min_length=1)]
