from __future__ import annotations

from collections.abc import Mapping, Set as AbstractSet
from typing import Final, final

from typing_extensions import override

from ._collections import DelegatingMutableMapping
from ._cube_mask_condition import CubeMaskCondition
from ._java_api import JavaApi
from ._operation import disjunctive_normal_form_from_condition
from ._require_live_extension import require_live_extension


@final
class Masks(DelegatingMutableMapping[str, CubeMaskCondition]):
    def __init__(self, /, *, cube_name: str, java_api: JavaApi | None) -> None:
        self._cube_name: Final = cube_name
        self._java_api: Final = java_api

    @override
    def _get_delegate(self, *, key: str | None) -> Mapping[str, CubeMaskCondition]:
        java_api = require_live_extension(self._java_api)
        return java_api.get_cube_mask(key, cube_name=self._cube_name)

    @override
    def _update_delegate(self, other: Mapping[str, CubeMaskCondition], /) -> None:
        java_api = require_live_extension(self._java_api)

        for role_name, condition in other.items():
            (conjunct_conditions,) = disjunctive_normal_form_from_condition(condition)
            includes = {}
            excludes = {}

            for leaf_condition in conjunct_conditions:
                match leaf_condition.operator:
                    case "IS_IN":
                        includes[leaf_condition.subject._java_description] = (
                            leaf_condition.member_paths
                        )
                    case "IS_NOT_IN":
                        excludes[leaf_condition.subject._java_description] = (
                            leaf_condition.member_paths
                        )

            java_api.set_cube_mask(
                includes,
                excludes,
                cube_name=self._cube_name,
                role_name=role_name,
            )

    @override
    def _delete_delegate_keys(self, keys: AbstractSet[str], /) -> None:
        raise NotImplementedError("Cannot delete masking value.")
