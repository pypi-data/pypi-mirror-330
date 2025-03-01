from collections.abc import Mapping, Set as AbstractSet
from typing import Final, final

from typing_extensions import override

from ._collections import DelegatingMutableMapping
from ._java_api import JavaApi
from ._require_live_extension import require_live_extension
from .aggregate_provider import AggregateProvider


@final
class AggregateProviders(DelegatingMutableMapping[str, AggregateProvider]):
    def __init__(self, *, cube_name: str, java_api: JavaApi | None):
        self._cube_name: Final = cube_name
        self._java_api: Final = java_api

    @override
    def _get_delegate(
        self,
        *,
        key: str | None,
    ) -> Mapping[str, AggregateProvider]:
        java_api = require_live_extension(self._java_api)
        return java_api.get_aggregate_providers_attributes(
            cube_name=self._cube_name,
            key=key,
        )

    @override
    def _update_delegate(self, other: Mapping[str, AggregateProvider], /) -> None:
        java_api = require_live_extension(self._java_api)
        java_api.add_aggregate_providers(other, cube_name=self._cube_name)
        java_api.refresh()

    @override
    def _delete_delegate_keys(self, keys: AbstractSet[str], /) -> None:
        java_api = require_live_extension(self._java_api)
        java_api.remove_aggregate_providers(keys, cube_name=self._cube_name)
        java_api.refresh()
