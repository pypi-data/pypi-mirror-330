from collections.abc import Set as AbstractSet
from typing import Final, final

from typing_extensions import override

from .._atoti_client import AtotiClient
from .._check_named_object_defined import check_named_object_defined
from .._identification import (
    HasIdentifier,
    LevelIdentifier,
    QueryCubeIdentifier,
    QueryCubeName,
)
from .._ipython import ReprJson, ReprJsonable
from .._java_api import JavaApi
from .._require_live_extension import require_live_extension


# Only add methods and properties to this class if they are specific to query cubes.
# See comment in `BaseSession` for more information.
@final
class QueryCube(HasIdentifier[QueryCubeIdentifier], ReprJsonable):
    r"""A query cube of a :class:`~atoti.QuerySession`."""

    def __init__(
        self,
        identifier: QueryCubeIdentifier,
        /,
        *,
        atoti_client: AtotiClient,
        java_api: JavaApi | None,
    ):
        self._atoti_client: Final = atoti_client
        self.__identifier: Final = identifier
        self._java_api: Final = java_api

    @property
    @override
    def _identifier(self) -> QueryCubeIdentifier:
        return self.__identifier

    @property
    def name(self) -> QueryCubeName:
        """The name of the query cube."""
        return self._identifier.cube_name

    @property
    def distributing_levels(self) -> AbstractSet[LevelIdentifier]:
        """The identifiers of the levels distributing data across the data cubes connecting to the query cube.

        Each level is independently considered as a partitioning key.
        This means that for a query cube configured with ``distributing_levels={date_level_key, region_level_key}``, each data cube must contribute a unique :guilabel:`date`, not present in any other data cube, as well as a unique :guilabel:`region`.
        """
        java_api = require_live_extension(self._java_api)
        levels = java_api.get_distributing_levels(self._identifier)
        return frozenset(
            LevelIdentifier._parse_java_description(level_description)
            for level_description in levels
        )

    @property
    def data_cube_ids(self) -> AbstractSet[str]:
        """Opaque IDs representing each data cubes connected to this query cube."""
        graphql_client = require_live_extension(self._atoti_client._graphql_client)
        cluster = check_named_object_defined(
            graphql_client.get_cluster_members(self.name).data_model.cube,
            "query cube",
            self.name,
        ).cluster
        return (
            frozenset()
            if cluster is None
            else frozenset(node.name for node in cluster.nodes)
        )

    @override
    def _repr_json_(self) -> ReprJson:
        return (
            {"name": self.name},
            {"expanded": False, "root": self.name},
        )
