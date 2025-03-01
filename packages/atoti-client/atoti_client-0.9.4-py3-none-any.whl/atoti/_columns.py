from typing import Final, final

from typing_extensions import override

from ._atoti_client import AtotiClient
from ._check_named_object_defined import check_named_object_defined
from ._collections import (
    DelegatingKeyDisambiguatingMapping,
    SupportsUncheckedMappingLookup,
)
from ._identification import ColumnIdentifier, ColumnName, TableIdentifier
from ._require_live_extension import require_live_extension
from .column import Column


@final
class Columns(
    SupportsUncheckedMappingLookup[ColumnName, ColumnName, Column],
    DelegatingKeyDisambiguatingMapping[ColumnName, ColumnName, Column],
):
    def __init__(
        self, *, atoti_client: AtotiClient, table_identifier: TableIdentifier
    ) -> None:
        self._atoti_client: Final = atoti_client
        self._table_identifier: Final = table_identifier

    @override
    def _create_lens(self, key: ColumnName, /) -> Column:
        return Column(
            ColumnIdentifier(self._table_identifier, key),
            atoti_client=self._atoti_client,
        )

    @override
    def _get_unambiguous_keys(self, *, key: ColumnName | None) -> list[ColumnName]:
        graphql_client = require_live_extension(self._atoti_client._graphql_client)

        if key is None:
            table = check_named_object_defined(
                graphql_client.get_table_columns(
                    table_name=self._table_identifier.table_name,
                ).data_model.table,
                "table",
                self._table_identifier.table_name,
            )
            return [column.name for column in table.columns]

        table = check_named_object_defined(  # type: ignore[assignment]
            graphql_client.find_column(
                column_name=key,
                table_name=self._table_identifier.table_name,
            ).data_model.table,
            "table",
            self._table_identifier.table_name,
        )
        column = check_named_object_defined(  # type: ignore[var-annotated]
            table.column,  # type: ignore[attr-defined]
            "column",
            key,
            error_type=KeyError,
        )
        return [column.name]
