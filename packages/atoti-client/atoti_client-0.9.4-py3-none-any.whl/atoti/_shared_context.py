from __future__ import annotations

from collections.abc import Mapping, Set as AbstractSet
from typing import Final, final

from typing_extensions import override

from ._collections import DelegatingMutableMapping
from ._ipython import ReprJson, ReprJsonable
from ._java_api import JavaApi
from ._require_live_extension import require_live_extension


@final
class SharedContext(DelegatingMutableMapping[str, str], ReprJsonable):  # type: ignore[misc]
    def __init__(self, *, cube_name: str, java_api: JavaApi | None) -> None:
        self._cube_name: Final = cube_name
        self._java_api: Final = java_api

    @override
    def _get_delegate(self, *, key: str | None) -> Mapping[str, str]:
        java_api = require_live_extension(self._java_api)
        return java_api.get_shared_context_values(
            cube_name=self._cube_name,
            key=key,
        )

    @override
    def _update_delegate(self, other: Mapping[str, str], /) -> None:
        java_api = require_live_extension(self._java_api)
        for key, value in other.items():
            java_api.set_shared_context_value(
                key,
                str(value),
                cube_name=self._cube_name,
            )
        java_api.refresh()

    @override
    def _delete_delegate_keys(self, keys: AbstractSet[str], /) -> None:
        raise NotImplementedError("Cannot delete context value.")

    @override
    def _repr_json_(self) -> ReprJson:
        return (
            dict(self),
            {"expanded": True, "root": "Context Values"},
        )
