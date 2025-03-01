from collections import defaultdict
from collections.abc import Sequence
from math import ceil
from typing import final

import pandas as pd
from typing_extensions import TypedDict

from .._activeviam_client import ActiveViamClient
from .._gaq_filter_condition import GaqFilterCondition, _GaqFilterLeafCondition
from .._identification import LevelIdentifier, MeasureIdentifier
from .._operation import (
    IsInCondition,
    RelationalCondition,
    disjunctive_normal_form_from_condition,
)
from .._typing import Duration
from ._execute_arrow_query import execute_arrow_query


@final
class _GaqOptions(TypedDict):
    equalConditions: dict[str, str]
    isinConditions: dict[str, list[str]]
    neConditions: dict[str, list[str]]


def _gaq_options_from_gaq_filter(
    condition: GaqFilterCondition | None,
    /,
) -> _GaqOptions:
    serialized_conditions: _GaqOptions = {
        "equalConditions": {},
        "isinConditions": defaultdict(list),
        "neConditions": defaultdict(list),
    }

    if condition is None:
        return serialized_conditions

    dnf: tuple[tuple[_GaqFilterLeafCondition, ...]] = (
        disjunctive_normal_form_from_condition(condition)
    )

    for leaf_condition in dnf[0]:
        match leaf_condition:
            case IsInCondition(
                subject=subject,
                operator="IS_IN",  # `IS_NOT_IN` is not supported.
            ):
                serialized_conditions["isinConditions"][
                    subject._java_description
                ].extend(
                    [
                        str(element._legacy_value_json)
                        for element in leaf_condition._sorted_elements
                    ]
                )
            case RelationalCondition(subject=subject, operator=operator, target=target):
                match operator:
                    case "EQ":
                        serialized_conditions["equalConditions"][
                            subject._java_description
                        ] = str(target._legacy_value_json)
                    case "NE":
                        serialized_conditions["neConditions"][
                            subject._java_description
                        ].append(str(target._legacy_value_json))

    return serialized_conditions


def execute_gaq(
    *,
    activeviam_client: ActiveViamClient,
    cube_name: str,
    filter: GaqFilterCondition | None,  # noqa: A002
    level_identifiers: Sequence[LevelIdentifier],
    measure_identifiers: Sequence[MeasureIdentifier],
    scenario_name: str | None,
    timeout: Duration,
) -> pd.DataFrame:
    body = {
        "cubeName": cube_name,
        "branch": scenario_name,
        "measures": [
            measure_identifier.measure_name
            for measure_identifier in measure_identifiers
        ],
        "levelCoordinates": [
            level_identifier._java_description for level_identifier in level_identifiers
        ],
        **_gaq_options_from_gaq_filter(filter),
        "timeout": ceil(timeout.total_seconds()),
    }

    path = activeviam_client.get_endpoint_path(namespace="atoti", route="arrow/query")

    return execute_arrow_query(
        activeviam_client=activeviam_client,
        body=body,
        path=path,
    )
