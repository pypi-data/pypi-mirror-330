from collections.abc import Callable, Mapping, Set as AbstractSet
from typing import Final, final

from typing_extensions import override

from .._collections import DelegatingConvertingMapping, SupportsUncheckedMappingLookup
from .._identification import ClusterIdentifier, ClusterName
from .._ipython import ReprJson, ReprJsonable
from .._java_api import JavaApi
from .._require_live_extension import require_live_extension
from ..cluster_definition import ClusterDefinition
from .cluster import Cluster


@final
class Clusters(
    SupportsUncheckedMappingLookup[ClusterName, ClusterName, Cluster],
    DelegatingConvertingMapping[ClusterName, ClusterName, Cluster, ClusterDefinition],
    ReprJsonable,
):
    def __init__(
        self, *, trigger_auto_join: Callable[[], bool], java_api: JavaApi | None
    ):
        self._trigger_auto_join: Final = trigger_auto_join
        self._java_api: Final = java_api

    @override
    def _create_lens(self, key: ClusterName, /) -> Cluster:
        return Cluster(ClusterIdentifier(key), java_api=self._java_api)

    @override
    def _get_unambiguous_keys(self, *, key: ClusterName | None) -> list[ClusterName]:
        java_api = require_live_extension(self._java_api)
        return [identifier.cluster_name for identifier in java_api.get_clusters()]

    @override
    def _update_delegate(self, other: Mapping[ClusterName, ClusterDefinition]) -> None:
        java_api = require_live_extension(self._java_api)
        for cluster_name, cluster_config in other.items():
            java_api.create_distributed_cluster(
                cluster_name=cluster_name,
                cluster_config=cluster_config,
            )

        java_api.refresh()
        if self._trigger_auto_join():
            java_api.auto_join_new_distributed_clusters(cluster_names=other.keys())
            java_api.refresh()

    @override
    def _delete_delegate_keys(self, keys: AbstractSet[ClusterName], /) -> None:
        java_api = require_live_extension(self._java_api)
        for key in keys:
            java_api.delete_cluster(ClusterIdentifier(key))

        java_api.refresh()

    @override
    def _repr_json_(self) -> ReprJson:
        return (
            {name: cluster._repr_json_()[0] for name, cluster in sorted(self.items())},
            {"expanded": False, "root": "Clusters"},
        )
