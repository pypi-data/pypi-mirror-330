from collections.abc import Mapping, Set as AbstractSet
from typing import Final, final

from typing_extensions import override

from ._collections import DelegatingMutableMapping
from ._identification import ColumnIdentifier, Identifiable, LevelIdentifier
from ._java_api import JavaApi
from ._require_live_extension import require_live_extension


@final
class MemberProperties(DelegatingMutableMapping[str, Identifiable[ColumnIdentifier]]):
    def __init__(
        self,
        *,
        cube_name: str,
        level_identifier: LevelIdentifier,
        java_api: JavaApi | None,
    ):
        self._cube_name: Final = cube_name
        self._level_identifier: Final = level_identifier
        self._java_api: Final = java_api

    @override
    def _get_delegate(
        self,
        *,
        key: str | None,
    ) -> Mapping[str, Identifiable[ColumnIdentifier]]:
        java_api = require_live_extension(self._java_api)
        return java_api.get_member_properties(
            self._level_identifier,
            cube_name=self._cube_name,
            key=key,
        )

    @override
    def _update_delegate(
        self,
        other: Mapping[str, Identifiable[ColumnIdentifier]],
        /,
    ) -> None:
        java_api = require_live_extension(self._java_api)
        new_value = {**self, **other}
        java_api.set_member_properties(
            self._level_identifier,
            new_value,
            cube_name=self._cube_name,
        )
        java_api.refresh()

    @override
    def _delete_delegate_keys(self, keys: AbstractSet[str], /) -> None:
        java_api = require_live_extension(self._java_api)

        new_value = {**self}
        for key in keys:
            del new_value[key]

        java_api.set_member_properties(
            self._level_identifier,
            new_value,
            cube_name=self._cube_name,
        )
        java_api.refresh()
