from typing import Final, final

from typing_extensions import override

from .._identification import (
    ApplicationNames,
    ClusterIdentifier,
    ClusterName,
    HasIdentifier,
)
from .._ipython import ReprJson, ReprJsonable
from .._java_api import JavaApi
from .._require_live_extension import require_live_extension
from ..distribution_protocols import DiscoveryProtocol


@final
class Cluster(HasIdentifier[ClusterIdentifier], ReprJsonable):
    def __init__(self, identifier: ClusterIdentifier, /, *, java_api: JavaApi | None):
        self.__identifier: Final = identifier
        self._java_api: Final = java_api

    @property
    def name(self) -> ClusterName:
        """The name of the cluster."""
        return self._identifier.cluster_name

    @property
    def application_names(self) -> ApplicationNames:
        """The names of the applications allowed to join the cluster."""
        java_api = require_live_extension(self._java_api)
        return frozenset(java_api.get_cluster_application_names(self._identifier))

    # This always returns `None` or a `CustomDiscoveryProtocol`.
    # Do not make this public until it instead returns the same class as the one that was passed to `ClusterDefinition`.
    @property
    def _discovery_protocol(self) -> DiscoveryProtocol | None:
        """The discovery protocol used by the cluster."""
        java_api = require_live_extension(self._java_api)
        return java_api.get_cluster_discovery_protocol(self._identifier)

    @property
    @override
    def _identifier(self) -> ClusterIdentifier:
        return self.__identifier

    @override
    def _repr_json_(self) -> ReprJson:
        return (
            {
                "name": self.name,
                "application_names": self.application_names,
            },
            {"expanded": False, "root": self.name},
        )
