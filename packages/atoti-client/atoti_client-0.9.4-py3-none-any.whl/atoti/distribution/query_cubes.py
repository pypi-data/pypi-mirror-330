from collections.abc import Mapping, Set as AbstractSet
from typing import Final, final

from typing_extensions import override

from .._atoti_client import AtotiClient
from .._collections import DelegatingConvertingMapping, SupportsUncheckedMappingLookup
from .._identification import QueryCubeIdentifier, QueryCubeName, identify
from .._identification.level_key import java_description_from_level_key
from .._ipython import ReprJson, ReprJsonable
from .._java_api import JavaApi
from .._require_live_extension import require_live_extension
from .query_cube import QueryCube
from .query_cube_definition import QueryCubeDefinition


@final
class QueryCubes(
    SupportsUncheckedMappingLookup[QueryCubeName, QueryCubeName, QueryCube],
    DelegatingConvertingMapping[
        QueryCubeName, QueryCubeName, QueryCube, QueryCubeDefinition
    ],
    ReprJsonable,
):
    r"""Manage the :class:`~atoti.QueryCube`\ s of a :class:`~atoti.QuerySession`."""

    def __init__(
        self,
        *,
        atoti_client: AtotiClient,
        java_api: JavaApi | None,
    ):
        self._atoti_client: Final = atoti_client
        self._java_api: Final = java_api

    @override
    def _create_lens(self, key: QueryCubeName, /) -> QueryCube:
        return QueryCube(
            QueryCubeIdentifier(key),
            atoti_client=self._atoti_client,
            java_api=self._java_api,
        )

    @override
    def _get_unambiguous_keys(
        self, *, key: QueryCubeName | None
    ) -> list[QueryCubeName]:
        graphql_client = require_live_extension(self._atoti_client._graphql_client)

        if key is None:
            return [cube.name for cube in graphql_client.get_cubes().data_model.cubes]

        cube = graphql_client.find_cube(
            cube_name=key,
        ).data_model.cube
        return [cube.name] if cube else []

    @override
    def _update_delegate(
        self,
        other: Mapping[QueryCubeName, QueryCubeDefinition],
        /,
    ) -> None:
        java_api = require_live_extension(self._java_api)
        for cube_name, cube_definition in other.items():
            cluster_identifier = identify(cube_definition.cluster)
            application_names = cube_definition.application_names

            if application_names is None:
                application_names = java_api.get_cluster_application_names(
                    cluster_identifier
                )

            java_api.create_query_cube(
                cube_name,
                application_names=application_names,
                catalog_names=cube_definition.catalog_names,
                cluster_name=cluster_identifier.cluster_name,
                distribution_levels=[
                    java_description_from_level_key(lvl)
                    for lvl in cube_definition.distributing_levels
                ],
            )
        java_api.refresh()

    @override
    def _delete_delegate_keys(self, keys: AbstractSet[QueryCubeName], /) -> None:
        raise NotImplementedError("Deleting query cubes is not supported yet.")

    @override
    def _repr_json_(self) -> ReprJson:
        return (
            {name: cube._repr_json_()[0] for name, cube in self.items()},
            {"expanded": False, "root": "Cubes"},
        )
