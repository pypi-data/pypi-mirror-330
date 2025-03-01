from dataclasses import KW_ONLY
from typing import final

from pydantic.dataclasses import dataclass
from typing_extensions import Self, override

from .._graphql_client import LevelIdentifier as GraphqlLevelIdentifier
from ._identifier_pydantic_config import IDENTIFIER_PYDANTIC_CONFIG
from .dimension_name import DimensionName
from .hierarchy_identifier import HierarchyIdentifier
from .hierarchy_name import HierarchyName
from .identifier import Identifier
from .level_key import (
    java_description_from_level_key,
    level_key_from_java_description,
    normalize_level_key,
)
from .level_name import LevelName


@final
@dataclass(config=IDENTIFIER_PYDANTIC_CONFIG, frozen=True)
class LevelIdentifier(Identifier):
    hierarchy_identifier: HierarchyIdentifier
    level_name: LevelName
    _: KW_ONLY

    @classmethod
    def _from_graphql(cls, level_identifier: GraphqlLevelIdentifier, /) -> Self:
        return cls(
            HierarchyIdentifier._from_graphql(level_identifier.hierarchy),
            level_identifier.name,
        )

    @classmethod
    def _parse_java_description(cls, java_description: str, /) -> Self:
        dimension_name, hierarchy_name, level_name = normalize_level_key(
            level_key_from_java_description(java_description)
        )
        assert dimension_name is not None
        assert hierarchy_name is not None
        return cls(HierarchyIdentifier(dimension_name, hierarchy_name), level_name)

    @property
    def _java_description(self) -> str:
        return java_description_from_level_key(self.key)

    @property
    def key(self) -> tuple[DimensionName, HierarchyName, LevelName]:
        return *self.hierarchy_identifier.key, self.level_name

    @override
    def __repr__(self) -> str:
        return f"l[{', '.join(repr(part) for part in self.key)}]"
