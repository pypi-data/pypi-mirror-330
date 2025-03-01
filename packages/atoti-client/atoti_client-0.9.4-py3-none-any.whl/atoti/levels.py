from __future__ import annotations

import operator
from typing import Final, final

from typing_extensions import override

from ._atoti_client import AtotiClient
from ._check_named_object_defined import check_named_object_defined
from ._collections import (
    DelegatingKeyDisambiguatingMapping,
    SupportsUncheckedMappingLookup,
)
from ._identification import (
    RESERVED_DIMENSION_NAMES as _RESERVED_DIMENSION_NAMES,
    CubeIdentifier,
    HierarchyIdentifier,
    LevelIdentifier,
    LevelKey,
    LevelUnambiguousKey,
)
from ._identification.level_key import normalize_level_key
from ._ipython import KeyCompletable, ReprJson, ReprJsonable
from ._java_api import JavaApi
from ._require_live_extension import require_live_extension
from .hierarchies import Hierarchies
from .level import Level


@final
class Levels(
    SupportsUncheckedMappingLookup[LevelKey, LevelUnambiguousKey, Level],
    DelegatingKeyDisambiguatingMapping[LevelKey, LevelUnambiguousKey, Level],
    KeyCompletable,
    ReprJsonable,
):
    r"""Flat representation of all the :class:`~atoti.Level`\ s in a :class:`~atoti.Cube`."""

    def __init__(
        self,
        *,
        atoti_client: AtotiClient,
        cube_identifier: CubeIdentifier,
        hierarchies: Hierarchies,
        java_api: JavaApi | None,
    ) -> None:
        self._atoti_client: Final = atoti_client
        self._cube_identifier: Final = cube_identifier
        self._hierarchies: Final = hierarchies
        self._java_api: Final = java_api

    @override
    def _create_lens(self, key: LevelUnambiguousKey, /) -> Level:
        return Level(
            LevelIdentifier(
                HierarchyIdentifier(key[0], key[1]),
                key[2],
            ),
            atoti_client=self._atoti_client,
            cube_identifier=self._cube_identifier,
            java_api=self._java_api,
        )

    @override
    def _get_unambiguous_keys(  # noqa: PLR0911
        self, *, key: LevelKey | None
    ) -> list[LevelUnambiguousKey]:
        dimension_name, hierarchy_name, level_name = (
            (None, None, None) if key is None else normalize_level_key(key)
        )

        # Remove `not self._java_api` once query sessions are supported.
        if not self._java_api or not self._atoti_client._graphql_client:
            cube_discovery = self._atoti_client.get_cube_discovery()
            return [
                (dimension.name, hierarchy.name, level.name)
                for dimension in cube_discovery.cubes[
                    self._cube_identifier.cube_name
                ].dimensions
                if dimension.name not in _RESERVED_DIMENSION_NAMES
                and (dimension_name is None or dimension.name == dimension_name)
                for hierarchy in dimension.hierarchies
                if hierarchy_name is None or hierarchy.name == hierarchy_name
                for level in hierarchy.levels
                if (level.type != "ALL")
                and (level_name is None or level.name == level_name)
            ]

        if level_name is None:
            cube = check_named_object_defined(
                self._atoti_client._graphql_client.get_levels(
                    cube_name=self._cube_identifier.cube_name,
                ).data_model.cube,
                "cube",
                self._cube_identifier.cube_name,
            )
            return [
                (dimension.name, hierarchy.name, level.name)
                for dimension in cube.dimensions
                if dimension.name not in _RESERVED_DIMENSION_NAMES
                for hierarchy in dimension.hierarchies
                for level in hierarchy.levels
                if level.type.value != "ALL"
            ]

        if hierarchy_name is None:
            cube = check_named_object_defined(  # type: ignore[assignment]
                self._atoti_client._graphql_client.find_level_across_hierarchies(
                    cube_name=self._cube_identifier.cube_name,
                    level_name=level_name,
                ).data_model.cube,
                "cube",
                self._cube_identifier.cube_name,
            )
            return [
                (
                    dimension.name,
                    hierarchy.name,
                    hierarchy.level.name,  # type: ignore[attr-defined]
                )
                for dimension in cube.dimensions
                if dimension.name not in _RESERVED_DIMENSION_NAMES
                for hierarchy in dimension.hierarchies
                if hierarchy.level and hierarchy.level.type.value != "ALL"  # type: ignore[attr-defined]
            ]

        if dimension_name is None:
            cube = check_named_object_defined(  # type: ignore[assignment]
                self._atoti_client._graphql_client.find_level_across_dimensions(
                    cube_name=self._cube_identifier.cube_name,
                    hierarchy_name=hierarchy_name,
                    level_name=level_name,
                ).data_model.cube,
                "cube",
                self._cube_identifier.cube_name,
            )
            return [
                (
                    dimension.name,
                    dimension.hierarchy.name,  # type: ignore[attr-defined]
                    dimension.hierarchy.level.name,  # type: ignore[attr-defined]
                )
                for dimension in cube.dimensions
                if dimension.name not in _RESERVED_DIMENSION_NAMES
                and dimension.hierarchy  # type: ignore[attr-defined]
                and dimension.hierarchy.level  # type: ignore[attr-defined]
                and dimension.hierarchy.level.type.value != "ALL"  # type: ignore[attr-defined]
            ]

        cube = check_named_object_defined(  # type: ignore[assignment]
            self._atoti_client._graphql_client.find_level(
                cube_name=self._cube_identifier.cube_name,
                dimension_name=dimension_name,
                hierarchy_name=hierarchy_name,
                level_name=level_name,
            ).data_model.cube,
            "cube",
            self._cube_identifier.cube_name,
        )
        dimension = check_named_object_defined(  # type: ignore[var-annotated]
            cube.dimension,  # type: ignore[attr-defined]
            "dimension",
            dimension_name,
            error_type=KeyError,
        )

        if dimension.name in _RESERVED_DIMENSION_NAMES:
            return []

        hierarchy = check_named_object_defined(  # type: ignore[var-annotated]
            dimension.hierarchy,
            "hierarchy",
            hierarchy_name,
            error_type=KeyError,
        )
        level = check_named_object_defined(
            hierarchy.level,  # type: ignore[var-annotated]
            "level",
            level_name,
            error_type=KeyError,
        )

        if level.type.value == "ALL":
            return []

        return [(dimension.name, hierarchy.name, level.name)]

    @override
    def _repr_json_(self) -> ReprJson:
        # Use the dimension/hierarchy/level in the map key to make it unique.
        data = {
            f"{level.name} ({level.dimension}/{level.hierarchy})": level._repr_json_()[
                0
            ]
            for hierarchy in self._hierarchies.values()
            for level in hierarchy.values()
        }
        sorted_data = dict(sorted(data.items(), key=operator.itemgetter(0)))
        return (
            sorted_data,
            {
                "expanded": True,
                "root": "Levels",
            },
        )

    def __delitem__(self, key: LevelKey, /) -> None:
        # Same signature as `MutableMapping.__delitem__()`.
        level = self[key]
        java_api = require_live_extension(level._java_api)
        java_api.delete_level(
            level._identifier,
            cube_name=self._cube_identifier.cube_name,
        )
        java_api.refresh()
