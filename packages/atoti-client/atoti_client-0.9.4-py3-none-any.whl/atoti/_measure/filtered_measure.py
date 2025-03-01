from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass
from typing import Literal, final

from typing_extensions import override

from .._constant import Constant
from .._data_type import DataType, is_primitive_type
from .._identification import LevelIdentifier, MeasureIdentifier
from .._java_api import JavaApi
from .._measure_description import MeasureDescription
from .._operation import (
    HierarchyIsInCondition,
    IsInCondition,
    LogicalCondition,
    RelationalCondition,
    RelationalConditionOperatorBound,
    disjunctive_normal_form_from_condition,
)
from .._py4j_utils import to_java_list, to_java_object


def is_object_type(data_type: DataType, /) -> bool:
    return not is_primitive_type(data_type)


@final
@dataclass(eq=False, frozen=True, kw_only=True)
class WhereMeasure(MeasureDescription):
    """A measure that returns the value of other measures based on conditions."""

    _conditions_to_target_measure: Sequence[
        tuple[MeasureDescription, MeasureDescription]
    ]
    _default_measure: MeasureDescription | None

    @override
    def _do_distil(
        self,
        identifier: MeasureIdentifier | None = None,
        /,
        *,
        java_api: JavaApi,
        cube_name: str,
    ) -> MeasureIdentifier:
        underlying_default_measure = (
            self._default_measure._distil(
                java_api=java_api,
                cube_name=cube_name,
            ).measure_name
            if self._default_measure is not None
            else None
        )

        return java_api.create_measure(
            identifier,
            "WHERE",
            {
                (
                    condition._distil(
                        java_api=java_api,
                        cube_name=cube_name,
                    ).measure_name
                ): measure._distil(
                    java_api=java_api,
                    cube_name=cube_name,
                ).measure_name
                for condition, measure in self._conditions_to_target_measure
            },
            underlying_default_measure,
            cube_name=cube_name,
        )


_FilterLeafCondition = (
    HierarchyIsInCondition[Literal["IS_IN"]]
    | IsInCondition[LevelIdentifier, Literal["IS_IN"], Constant]
    | RelationalCondition[LevelIdentifier, RelationalConditionOperatorBound, Constant]
)
FilterCondition = (
    _FilterLeafCondition | LogicalCondition[_FilterLeafCondition, Literal["AND"]]
)


@final
@dataclass(eq=False, frozen=True, kw_only=True)
class LevelValueFilteredMeasure(MeasureDescription):
    """A measure on a part of the cube filtered on a level value."""

    _underlying_measure: MeasureDescription
    _filter: FilterCondition

    @override
    def _do_distil(
        self,
        identifier: MeasureIdentifier | None = None,
        /,
        *,
        cube_name: str,
        java_api: JavaApi,
    ) -> MeasureIdentifier:
        underlying_name: str = self._underlying_measure._distil(
            java_api=java_api,
            cube_name=cube_name,
        ).measure_name

        dnf: tuple[tuple[_FilterLeafCondition, ...]] = (
            disjunctive_normal_form_from_condition(self._filter)
        )

        def _process(leaf_condition: _FilterLeafCondition, /) -> dict[str, object]:
            match leaf_condition:
                case RelationalCondition(
                    subject=subject, operator=operator, target=target
                ):
                    return {
                        "level": subject._java_description,
                        "type": "constant",
                        "operation": operator.lower(),
                        "value": to_java_object(
                            target.value,
                            gateway=java_api.gateway,
                        ),
                    }
                case IsInCondition(
                    subject=subject,
                    operator="IS_IN",  # `IS_NOT_IN` is not supported.
                ):
                    return {
                        "level": subject._java_description,
                        "type": "constant",
                        "operation": "li",
                        "value": to_java_list(
                            [
                                element.value
                                for element in leaf_condition._sorted_elements
                            ],
                            gateway=java_api.gateway,
                        ),
                    }
                case HierarchyIsInCondition(
                    subject=subject,
                    operator="IS_IN",  # `IS_NOT_IN` is not supported.
                    member_paths=member_paths,
                    level_names=level_names,
                ):
                    return {
                        "level": LevelIdentifier(
                            subject, level_names[0]
                        )._java_description,
                        "type": "constant",
                        "operation": "hi",
                        "value": [
                            {
                                LevelIdentifier(
                                    subject, level_name
                                )._java_description: member.value
                                for level_name, member in zip(
                                    level_names, member_path, strict=False
                                )
                            }
                            for member_path in sorted(member_paths)
                        ],
                    }

        conditions = [_process(leaf_condition) for leaf_condition in dnf[0]]

        # Create the filtered measure and return its name.
        return java_api.create_measure(
            identifier,
            "FILTER",
            underlying_name,
            conditions,
            cube_name=cube_name,
        )
