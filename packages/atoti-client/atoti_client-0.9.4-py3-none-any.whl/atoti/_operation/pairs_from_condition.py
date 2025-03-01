from typing import Literal

from .disjunctive_normal_form_from_condition import (
    disjunctive_normal_form_from_condition,
)
from .operation import (
    LogicalCondition,
    RelationalCondition,
    RelationalConditionSubjectT_co,
    RelationalConditionTargetT_co,
)


def pairs_from_condition(
    condition: RelationalCondition[
        RelationalConditionSubjectT_co,
        Literal["EQ"],
        RelationalConditionTargetT_co,
    ]
    | LogicalCondition[
        RelationalCondition[
            RelationalConditionSubjectT_co,
            Literal["EQ"],
            RelationalConditionTargetT_co,
        ],
        Literal["AND"],
    ],
    /,
) -> list[tuple[RelationalConditionSubjectT_co, RelationalConditionTargetT_co]]:
    dnf: tuple[
        tuple[
            RelationalCondition[
                RelationalConditionSubjectT_co,
                Literal["EQ"],
                RelationalConditionTargetT_co,
            ],
            ...,
        ]
    ] = disjunctive_normal_form_from_condition(condition)
    return [(condition.subject, condition.target) for condition in dnf[0]]
