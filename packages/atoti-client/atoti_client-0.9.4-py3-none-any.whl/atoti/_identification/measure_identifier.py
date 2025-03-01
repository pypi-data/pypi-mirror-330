from dataclasses import KW_ONLY
from typing import final

from pydantic.dataclasses import dataclass
from typing_extensions import override

from .._graphql_client import MeasureIdentifierInput
from ._identifier_pydantic_config import IDENTIFIER_PYDANTIC_CONFIG
from .identifier import Identifier
from .measure_name import MeasureName


@final
@dataclass(config=IDENTIFIER_PYDANTIC_CONFIG, frozen=True)
class MeasureIdentifier(Identifier):
    measure_name: MeasureName
    _: KW_ONLY

    @property
    def _graphql_input(self) -> MeasureIdentifierInput:
        return MeasureIdentifierInput(measure_name=self.measure_name)

    @override
    def __repr__(self) -> str:
        return f"m[{self.measure_name!r}]"
