from __future__ import annotations

from typing import Final, Literal, final, overload

from typing_extensions import override

from ._atoti_client import AtotiClient
from ._check_named_object_defined import check_named_object_defined
from ._constant import Constant, ConstantValue
from ._data_type import DataType, data_type_from_graphql
from ._graphql_client import (
    SetColumnDefaultValue,
    UpdateColumnAction,
    UpdateColumnInput,
)
from ._identification import ColumnIdentifier, ColumnName
from ._ipython import ReprJson, ReprJsonable
from ._operation import (
    IsInCondition,
    OperandConvertibleWithIdentifier,
    RelationalCondition,
)
from ._require_live_extension import require_live_extension


@final
class Column(
    OperandConvertibleWithIdentifier[ColumnIdentifier],
    ReprJsonable,
):
    """Column of a :class:`~atoti.Table`."""

    def __init__(
        self, identifier: ColumnIdentifier, /, *, atoti_client: AtotiClient
    ) -> None:
        self.__identifier: Final = identifier
        self._atoti_client: Final = atoti_client

    @property
    def name(self) -> ColumnName:
        """The name of the column."""
        return self._identifier.column_name

    @property
    def data_type(self) -> DataType:
        """The type of the elements in the column."""
        graphql_client = require_live_extension(self._atoti_client._graphql_client)
        table = check_named_object_defined(
            graphql_client.get_column_data_type(
                column_name=self.name,
                table_name=self._identifier.table_identifier.table_name,
            ).data_model.table,
            "table",
            self._identifier.table_identifier.table_name,
        )
        column = check_named_object_defined(
            table.column,
            "column",
            self.name,
        )
        return data_type_from_graphql(column.data_type)

    @property
    @override
    def _identifier(self) -> ColumnIdentifier:
        return self.__identifier

    @property
    @override
    def _operation_operand(self) -> ColumnIdentifier:
        return self._identifier

    @property
    def default_value(self) -> ConstantValue | None:
        """Value used to replace ``None`` inserted values.

        .. doctest::
            :hide:

            >>> session = getfixture("default_session")

        The default value can either be:

        * ``None``:

          >>> none_default_value_table = session.create_table(
          ...     "None",
          ...     data_types={"ZonedDateTime": "ZonedDateTime"},
          ...     default_values={"ZonedDateTime": None},
          ... )
          >>> none_default_value_table["ZonedDateTime"].default_value

        * a value matching the column's :attr:`~atoti.Column.data_type`:

          >>> from datetime import datetime
          >>> from zoneinfo import ZoneInfo
          >>> homogeneous_default_value_table = session.create_table(
          ...     "Homogeneous",
          ...     data_types={"ZonedDateTime": "ZonedDateTime"},
          ...     default_values={
          ...         "ZonedDateTime": datetime(
          ...             2025,
          ...             2,
          ...             13,
          ...             20,
          ...             58,
          ...             42,
          ...             tzinfo=ZoneInfo("America/New_York"),
          ...         )
          ...     },
          ... )
          >>> homogeneous_default_value_table["ZonedDateTime"].default_value
          datetime.datetime(2025, 2, 13, 20, 58, 42, tzinfo=zoneinfo.ZoneInfo(key='America/New_York'))
          >>> session.create_table(  # doctest: +ELLIPSIS
          ...     "Heterogeneous",
          ...     data_types={"ZonedDateTime": "ZonedDateTime"},
          ...     default_values={
          ...         # Stringified ZonedDateTimes are not accepted.
          ...         "ZonedDateTime": "2025-02-13T20:58:42-05:00[America/New_York]"
          ...     },
          ... )
          Traceback (most recent call last):
              ...
          atoti._graphql_client.exceptions.GraphQLClientGraphQLMultiError: Coercion from STRING to ZONED_DATE_TIME is not supported. ...
          >>> session.create_table(  # doctest: +ELLIPSIS
          ...     "Heterogeneous",
          ...     data_types={"ZonedDateTime": "ZonedDateTime"},
          ...     default_values={
          ...         # `"N/A"` is not accepted either.
          ...         "ZonedDateTime": "N/A"
          ...     },
          ... )
          Traceback (most recent call last):
              ...
          atoti._graphql_client.exceptions.GraphQLClientGraphQLMultiError: Coercion from STRING to ZONED_DATE_TIME is not supported. ...
          >>> session.create_table(  # doctest: +ELLIPSIS
          ...     "Heterogeneous",
          ...     data_types={"ZonedDateTime": "ZonedDateTime"},
          ...     default_values={
          ...         # ZonedDateTime values must have a zone info.
          ...         "ZonedDateTime": datetime(2025, 2, 13, 20, 58, 42)
          ...     },
          ... )
          Traceback (most recent call last):
              ...
          atoti._graphql_client.exceptions.GraphQLClientGraphQLMultiError: Coercion from LOCAL_DATE_TIME to ZONED_DATE_TIME is not supported. ...

        Each data type has its own default ``default_value`` value:

        >>> import pprint
        >>> all_data_types = [
        ...     "boolean",
        ...     "boolean[]",
        ...     "double",
        ...     "double[]",
        ...     "float",
        ...     "float[]",
        ...     "int",
        ...     "int[]",
        ...     "LocalDate",
        ...     "LocalDateTime",
        ...     "LocalTime",
        ...     "long",
        ...     "long[]",
        ...     "String",
        ...     "String[]",
        ...     "ZonedDateTime",
        ... ]
        >>> all_data_types_table = session.create_table(
        ...     "All",
        ...     data_types={data_type: data_type for data_type in all_data_types},
        ... )
        >>> pprint.pp(
        ...     {
        ...         column_name: all_data_types_table[column_name].default_value
        ...         for column_name in all_data_types_table
        ...     },
        ...     sort_dicts=False,
        ... )
        {'boolean': False,
         'boolean[]': None,
         'double': None,
         'double[]': None,
         'float': None,
         'float[]': None,
         'int': None,
         'int[]': None,
         'LocalDate': datetime.date(1970, 1, 1),
         'LocalDateTime': datetime.datetime(1970, 1, 1, 0, 0),
         'LocalTime': datetime.time(0, 0),
         'long': None,
         'long[]': None,
         'String': 'N/A',
         'String[]': None,
         'ZonedDateTime': datetime.datetime(1970, 1, 1, 0, 0, tzinfo=TzInfo(UTC))}

        .. doctest::
            :hide:

            >>> from atoti._data_type import _DATA_TYPE_ARGS
            >>> deprecated_data_types = {"Object", "Object[]"}
            >>> assert not (set(all_data_types) & deprecated_data_types)
            >>> assert (set(all_data_types) | deprecated_data_types) == (
            ...     set(_DATA_TYPE_ARGS)
            ... )

        Columns part of the table :attr:`~atoti.Table.keys` cannot have ``None`` as their default value.
        Key columns with:

        * a numeric scalar data type default to ``0``:

          >>> numeric_scalar_data_types = [
          ...     "double",
          ...     "float",
          ...     "int",
          ...     "long",
          ... ]
          >>> numeric_scalar_data_types_table = session.create_table(
          ...     "Numeric scalar",
          ...     data_types={
          ...         data_type: data_type for data_type in numeric_scalar_data_types
          ...     },
          ...     keys=numeric_scalar_data_types,
          ... )
          >>> {
          ...     column_name: numeric_scalar_data_types_table[
          ...         column_name
          ...     ].default_value
          ...     for column_name in numeric_scalar_data_types_table
          ... }
          {'double': 0.0, 'float': 0.0, 'int': 0, 'long': 0}
          >>> numeric_scalar_data_types_table += (None, None, None, None)
          >>> numeric_scalar_data_types_table.head()
          Empty DataFrame
          Columns: []
          Index: [(0.0, 0.0, 0, 0)]

        .. doctest::
            :hide:

            >>> from atoti._data_type import _NUMERIC_DATA_TYPE_ARGS
            >>> assert set(numeric_scalar_data_types) == set(_NUMERIC_DATA_TYPE_ARGS)

        * an array data type must have their default value specified:

          >>> array_data_types = ["int[]", "long[]", "float[]", "double[]"]
          >>> session.create_table(
          ...     "Array",
          ...     data_types={data_type: data_type for data_type in array_data_types},
          ...     keys=array_data_types,
          ... )
          Traceback (most recent call last):
              ...
          atoti._graphql_client.exceptions.GraphQLClientGraphQLMultiError: Cannot make a int[] non-nullable because there is no global default value defined for this type. You should manually define a default value.
          >>> array_data_types_table = session.create_table(
          ...     "Array",
          ...     data_types={data_type: data_type for data_type in array_data_types},
          ...     default_values={
          ...         "int[]": [1],
          ...         "long[]": [2],
          ...         "float[]": [3.0],
          ...         "double[]": [4.0],
          ...     },
          ...     keys={"int[]"},
          ... )
          >>> {
          ...     column_name: array_data_types_table[column_name].default_value
          ...     for column_name in array_data_types_table
          ... }
          {'int[]': (1,), 'long[]': (2,), 'float[]': (3.0,), 'double[]': (4.0,)}
          >>> array_data_types_table += (None, None, None, None)
          >>> array_data_types_table.head()
                long[] float[] double[]
          int[]
          [1]      [2]   [3.0]    [4.0]

        .. doctest::
            :hide:

            >>> from atoti._data_type import _ARRAY_DATA_TYPE_ARGS
            >>> deprecated_data_types = {"Object[]"}
            >>> data_types_behaving_incorrectly = {"boolean[]", "String[]"}
            >>> assert not (
            ...     set(array_data_types)
            ...     & (data_types_behaving_incorrectly | deprecated_data_types)
            ... )
            >>> assert (
            ...     set(array_data_types)
            ...     | data_types_behaving_incorrectly
            ...     | deprecated_data_types
            ... ) == (set(_ARRAY_DATA_TYPE_ARGS))

        Changing the default value from:

        * ``None`` to something else affects both the past ``None`` values and the future ones:

          >>> table = session.create_table(
          ...     "Change",
          ...     data_types={
          ...         "int[]": "int[]",
          ...         "long[]": "long[]",
          ...         "float": "float",
          ...         "String": "String",
          ...     },
          ...     default_values={
          ...         "int[]": [1],
          ...         "long[]": None,
          ...         "float": None,
          ...         "String": None,
          ...     },
          ...     keys={"int[]"},
          ... )
          >>> table += (None, None, None, None)
          >>> table["int[]"].default_value = [2]
          >>> table["long[]"].default_value = [3, 4, 5]
          >>> table["float"].default_value = 6.0
          >>> table["String"].default_value = "seven"
          >>> {column_name: table[column_name].default_value for column_name in table}
          {'int[]': (2,), 'long[]': (3, 4, 5), 'float': 6.0, 'String': 'seven'}
          >>> table += (None, None, None, None)
          >>> table.head().sort_index()
                    long[]  float String
          int[]
          [1]    [3, 4, 5]    6.0  seven
          [2]    [3, 4, 5]    6.0  seven

        * non-``None`` to something else does not affect the past values:

          >>> table["int[]"].default_value = [8]
          >>> table["long[]"].default_value = [9, 10, 11]
          >>> table["float"].default_value = 12.0
          >>> table["String"].default_value = "thirteen"
          >>> table += (None, None, None, None)
          >>> table.head().sort_index()
                      long[]  float    String
          int[]
          [1]      [3, 4, 5]    6.0     seven
          [2]      [3, 4, 5]    6.0     seven
          [8]    [9, 10, 11]   12.0  thirteen

        Changing the default value from non-``None`` to ``None`` is impossible both:

        * for key columns:

          >>> table["int[]"].default_value = None
          Traceback (most recent call last):
              ...
          atoti._graphql_client.exceptions.GraphQLClientGraphQLMultiError: Cannot define a null default value for a non-nullable type.
          >>> table["int[]"].default_value
          (8,)

        * and non-key columns:

          >>> table["float"].default_value = None
          Traceback (most recent call last):
              ...
          atoti._graphql_client.exceptions.GraphQLClientGraphQLMultiError: Cannot define a null default value for a non-nullable type.
          >>> table["float"].default_value
          12.0

        """
        graphql_client = require_live_extension(self._atoti_client._graphql_client)
        table = check_named_object_defined(
            graphql_client.get_column_default_value(
                column_name=self.name,
                table_name=self._identifier.table_identifier.table_name,
            ).data_model.table,
            "table",
            self._identifier.table_identifier.table_name,
        )
        default_value = check_named_object_defined(
            table.column,
            "column",
            self.name,
        ).default_value
        return None if default_value is None else default_value.value

    @default_value.setter
    def default_value(self, default_value: ConstantValue | None) -> None:
        graphql_client = require_live_extension(self._atoti_client._graphql_client)
        mutation_input = UpdateColumnInput(
            actions=[
                UpdateColumnAction(
                    set_default_value=SetColumnDefaultValue(
                        value=None
                        if default_value is None
                        else Constant.of(default_value),
                    ),
                ),
            ],
            column_identifier=self._identifier._graphql_input,
        )
        graphql_client.update_column(mutation_input)

    @overload
    def isin(
        self,
        *elements: ConstantValue,
    ) -> (
        IsInCondition[ColumnIdentifier, Literal["IS_IN"], Constant]
        | RelationalCondition[ColumnIdentifier, Literal["EQ"], Constant]
    ): ...

    @overload
    def isin(
        self,
        *elements: ConstantValue | None,
    ) -> (
        IsInCondition[ColumnIdentifier, Literal["IS_IN"], Constant | None]
        | RelationalCondition[ColumnIdentifier, Literal["EQ"], Constant | None]
    ): ...

    def isin(
        self,
        *elements: ConstantValue | None,
    ) -> (
        IsInCondition[ColumnIdentifier, Literal["IS_IN"], Constant | None]
        | RelationalCondition[ColumnIdentifier, Literal["EQ"], Constant | None]
    ):
        """Return a condition evaluating to ``True`` if a column element is among the given elements and ``False`` otherwise.

        ``table["City"].isin("Paris", "New York")`` is equivalent to ``(table["City"] == "Paris") | (table["City"] == "New York")``.

        Args:
            elements: One or more elements on which the column should be.
        """
        return IsInCondition.of(
            subject=self._operation_operand,
            operator="IS_IN",
            elements={
                None if element is None else Constant.of(element)
                for element in elements
            },
        )

    @override
    def _repr_json_(self) -> ReprJson:
        return {
            "type": self.data_type,
            "default_value": self.default_value
            if isinstance(self.default_value, type(None) | bool | int | float | str)
            else repr(self.default_value),
        }, {"expanded": True, "root": self.name}
