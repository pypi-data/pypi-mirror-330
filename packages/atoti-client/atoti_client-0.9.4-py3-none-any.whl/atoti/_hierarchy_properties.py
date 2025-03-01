from collections.abc import Mapping, Set as AbstractSet
from typing import Final, final

from pydantic import JsonValue
from typing_extensions import override

from ._collections import DelegatingMutableMapping
from ._identification import HierarchyIdentifier
from ._java_api import JavaApi
from ._require_live_extension import require_live_extension


@final
class HierarchyProperties(DelegatingMutableMapping[str, JsonValue]):
    def __init__(
        self,
        *,
        cube_name: str,
        hierarchy_identifier: HierarchyIdentifier,
        java_api: JavaApi | None,
    ):
        self._cube_name: Final = cube_name
        self._hierarchy_identifier: Final = hierarchy_identifier
        self._java_api: Final = java_api

    @override
    def _get_delegate(self, *, key: str | None) -> Mapping[str, JsonValue]:
        java_api = require_live_extension(self._java_api)
        return java_api.get_hierarchy_properties(
            self._hierarchy_identifier,
            cube_name=self._cube_name,
            key=key,
        )

    @override
    def _update_delegate(self, other: Mapping[str, JsonValue], /) -> None:
        java_api = require_live_extension(self._java_api)
        new_value = {**self, **other}
        java_api.set_hierarchy_properties(
            self._hierarchy_identifier,
            new_value,
            cube_name=self._cube_name,
        )
        java_api.refresh()

    @override
    def _delete_delegate_keys(self, keys: AbstractSet[str], /) -> None:
        java_api = require_live_extension(self._java_api)
        new_value = {**self}
        for key in keys or list(new_value):
            del new_value[key]
        java_api.set_hierarchy_properties(
            self._hierarchy_identifier,
            new_value,
            cube_name=self._cube_name,
        )
        java_api.refresh()
