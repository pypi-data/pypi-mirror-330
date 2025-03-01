from __future__ import annotations

from collections.abc import Mapping, Sequence, Set as AbstractSet
from typing import Final, TypeAlias, final

from typing_extensions import override

from ._atoti_client import AtotiClient
from ._check_named_object_defined import check_named_object_defined
from ._collections import DelegatingMutableMapping
from ._constant import Constant
from ._cube_restriction_condition import (
    CubeRestrictionCondition,
    _CubeRestrictionLeafCondition,
)
from ._graphql_client import (
    CubeRestrictionIsInConditionInput,
    CubeRestrictionIsInConditionOperator,
    CubeRestrictionLeafConditionInput,
    CubeRestrictionRelationalConditionInput,
    CubeRestrictionRelationalConditionOperator,
    DeleteCubeRestrictionsInput,
    GetCubeRestrictionsDataModelCubeRestrictionsConditionCubeRestrictionIsInCondition,
    GetCubeRestrictionsDataModelCubeRestrictionsConditionCubeRestrictionRelationalCondition,
    LevelIdentifierInput,
    UpdateCubeRestrictionsInput,
    UpdateCubeRestrictionsMappingItem,
)
from ._identification import CubeIdentifier, LevelIdentifier, RoleName
from ._operation import (
    IsInCondition,
    RelationalCondition,
    condition_from_disjunctive_normal_form,
    disjunctive_normal_form_from_condition,
)
from ._require_live_extension import require_live_extension
from ._reserved_roles import check_no_reserved_roles

_GraphQlCubeLeafCondition: TypeAlias = (
    GetCubeRestrictionsDataModelCubeRestrictionsConditionCubeRestrictionIsInCondition
    | GetCubeRestrictionsDataModelCubeRestrictionsConditionCubeRestrictionRelationalCondition
)


def _leaf_condition_from_graphql(
    condition: _GraphQlCubeLeafCondition, /
) -> _CubeRestrictionLeafCondition:
    match condition:
        case GetCubeRestrictionsDataModelCubeRestrictionsConditionCubeRestrictionIsInCondition():
            return IsInCondition.of(
                subject=LevelIdentifier._from_graphql(condition.level),
                operator=condition.is_in_operator.value,
                elements={Constant.of(element.value) for element in condition.elements},
            )
        case GetCubeRestrictionsDataModelCubeRestrictionsConditionCubeRestrictionRelationalCondition():
            return RelationalCondition(
                subject=LevelIdentifier._from_graphql(condition.level),
                operator=condition.relational_operator.value,
                target=condition.target,
            )


def _condition_from_graphql(
    dnf: Sequence[Sequence[_GraphQlCubeLeafCondition]],
    /,
) -> CubeRestrictionCondition:
    match dnf:
        case [graphql_conjunct_conditions]:
            conjunct_conditions = [
                _leaf_condition_from_graphql(condition)
                for condition in graphql_conjunct_conditions
            ]
            return condition_from_disjunctive_normal_form((conjunct_conditions,))
        case _:
            raise AssertionError(f"Unexpected disjunctive normal form: {dnf}.")


def _leaf_condition_to_graphql(
    condition: _CubeRestrictionLeafCondition, /
) -> CubeRestrictionLeafConditionInput:
    match condition:
        case IsInCondition():
            return CubeRestrictionLeafConditionInput(
                is_in=CubeRestrictionIsInConditionInput(
                    elements=list(condition.elements),
                    operator=CubeRestrictionIsInConditionOperator(condition.operator),
                    subject=LevelIdentifierInput(
                        dimension_name=condition.subject.hierarchy_identifier.dimension_name,
                        hierarchy_name=condition.subject.hierarchy_identifier.hierarchy_name,
                        level_name=condition.subject.level_name,
                    ),
                )
            )
        case RelationalCondition():
            return CubeRestrictionLeafConditionInput(
                relational=CubeRestrictionRelationalConditionInput(
                    operator=CubeRestrictionRelationalConditionOperator(
                        condition.operator
                    ),
                    subject=LevelIdentifierInput(
                        dimension_name=condition.subject.hierarchy_identifier.dimension_name,
                        hierarchy_name=condition.subject.hierarchy_identifier.hierarchy_name,
                        level_name=condition.subject.level_name,
                    ),
                    target=condition.target,
                )
            )


def _condition_to_graphql(
    condition: CubeRestrictionCondition, /
) -> list[list[CubeRestrictionLeafConditionInput]]:
    dnf = disjunctive_normal_form_from_condition(condition)
    return [
        [
            _leaf_condition_to_graphql(
                leaf_condition  # type: ignore[arg-type]
            )
            for leaf_condition in conjunct_conditions
        ]
        for conjunct_conditions in dnf
    ]


@final
class CubeRestrictions(DelegatingMutableMapping[RoleName, CubeRestrictionCondition]):
    def __init__(
        self, cube_identifier: CubeIdentifier, /, *, atoti_client: AtotiClient
    ) -> None:
        self._cube_identifier: Final = cube_identifier
        self._atoti_client: Final = atoti_client

    @override
    def _get_delegate(
        self, *, key: RoleName | None
    ) -> Mapping[str, CubeRestrictionCondition]:
        graphql_client = require_live_extension(self._atoti_client._graphql_client)
        cube = check_named_object_defined(
            graphql_client.get_cube_restrictions(
                cube_name=self._cube_identifier.cube_name
            ).data_model.cube,
            "cube",
            self._cube_identifier.cube_name,
        )
        return {
            restriction.role_name: _condition_from_graphql(restriction.condition)
            for restriction in cube.restrictions
        }

    @override
    def _update_delegate(
        self, other: Mapping[RoleName, CubeRestrictionCondition], /
    ) -> None:
        check_no_reserved_roles(other)
        graphql_client = require_live_extension(self._atoti_client._graphql_client)
        mutation_input = UpdateCubeRestrictionsInput(
            cube_identifier=self._cube_identifier._graphql_input,
            mapping_items=[
                UpdateCubeRestrictionsMappingItem(
                    condition=_condition_to_graphql(condition),
                    role_name=role_name,
                )
                for role_name, condition in other.items()
            ],
        )
        graphql_client.update_cube_restrictions(mutation_input)

    @override
    def _delete_delegate_keys(self, keys: AbstractSet[RoleName], /) -> None:
        graphql_client = require_live_extension(self._atoti_client._graphql_client)
        mutation_input = DeleteCubeRestrictionsInput(
            cube_identifier=self._cube_identifier._graphql_input,
            role_names=list(keys),
        )
        graphql_client.delete_cube_restrictions(mutation_input)
