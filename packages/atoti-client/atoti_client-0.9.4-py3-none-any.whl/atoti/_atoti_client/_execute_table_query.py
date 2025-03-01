from collections.abc import Sequence
from urllib.parse import quote, urlencode

import pandas as pd

from .._activeviam_client import ActiveViamClient
from .._column_description import ColumnDescription
from .._data_type import parse_data_type
from .._identification import TableName
from .._json_serializable_dict_from_condition import (
    json_serializable_dict_from_condition,
)
from .._pandas import create_dataframe
from .._table_query_filter_condition import TableQueryFilterCondition
from .._typing import Duration


def execute_table_query(
    *,
    activeviam_client: ActiveViamClient,
    column_descriptions: Sequence[ColumnDescription],
    filter: TableQueryFilterCondition | None = None,  # noqa: A002
    max_rows: int,
    scenario_name: str | None,
    table_name: TableName,
    timeout: Duration,
) -> pd.DataFrame:
    query = urlencode({"pageSize": max_rows})

    conditions = (
        json_serializable_dict_from_condition(filter) if filter is not None else {}
    )

    body = {
        "branch": scenario_name,
        "conditions": conditions,
        "fields": [
            column_description.name for column_description in column_descriptions
        ],
        # The server expects milliseconds.
        # See https://artifacts.activeviam.com/documentation/rest/6.0.3/activepivot-database.html#data_tables__tableName____query__post.
        "timeout": timeout.total_seconds() * 1000,
    }
    route = f"database/data/tables/{quote(table_name)}"

    path = f"{activeviam_client.get_endpoint_path(namespace='activeviam/pivot', route=route)}?{query}"
    response = activeviam_client.http_client.post(
        path,
        json=body,
        # The timeout is part of `body` and is managed by the server.
        timeout=None,
    ).raise_for_status()
    response_body = response.json()
    assert isinstance(response_body, dict)

    for header in response_body["headers"]:
        column_name = header["name"]
        received_data_type = parse_data_type(header["type"])
        expected_data_type = next(
            column_description.data_type
            for column_description in column_descriptions
            if column_description.name == column_name
        )
        assert expected_data_type == "Object" or (
            received_data_type == expected_data_type
        ), f"Unexpected data type for column `{column_name}`."

    return create_dataframe(
        response_body["rows"],
        column_descriptions,
    )
