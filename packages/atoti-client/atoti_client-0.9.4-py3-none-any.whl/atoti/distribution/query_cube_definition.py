from collections.abc import Set as AbstractSet
from typing import final

from pydantic.dataclasses import dataclass

from .._identification import (
    ApplicationNames,
    ClusterIdentifier,
    CubeCatalogNames,
    Identifiable,
)
from .._identification.level_key import LevelUnambiguousKey
from .._pydantic import PYDANTIC_CONFIG as _PYDANTIC_CONFIG


@final
@dataclass(config=_PYDANTIC_CONFIG, frozen=True, kw_only=True)
class QueryCubeDefinition:
    """The definition to create a :class:`~atoti.QueryCube`."""

    application_names: ApplicationNames | None = None
    """The names of the application allowed to contribute to the query cube.

    If ``None``, :attr:`cluster`'s :attr:`~atoti.ClusterDefinition.application_names` will be used.
    Otherwise, it must be a subset of that other set.

    :meta private:
    """

    catalog_names: CubeCatalogNames = frozenset({"atoti"})
    """The names of the catalogs in which the query cube will be.

    :meta private:
    """

    cluster: Identifiable[ClusterIdentifier]
    """Cluster joined by the query cube."""

    distributing_levels: AbstractSet[LevelUnambiguousKey] = frozenset()
    """The keys of the :attr:`~atoti.QueryCube.distributing_levels`."""
