from __future__ import annotations

from collections.abc import Callable, Set as AbstractSet
from contextlib import AbstractContextManager
from contextvars import ContextVar
from typing import Annotated, TypeAlias, final

from pydantic import Field
from pydantic.dataclasses import dataclass

from .._identification import TableIdentifier
from .._pydantic import PYDANTIC_CONFIG as _PYDANTIC_CONFIG
from ._transact import transact
from ._transaction_context import TransactionContext

DataTransactionTableIdentifiers: TypeAlias = Annotated[
    AbstractSet[TableIdentifier], Field(min_length=1)
]


@final
@dataclass(config=_PYDANTIC_CONFIG, frozen=True, kw_only=True)
class DataTransactionContext(TransactionContext):
    table_identifiers: DataTransactionTableIdentifiers | None


_CONTEXT_VAR: ContextVar[DataTransactionContext] = ContextVar(
    "atoti_data_transaction",
)


def data_transaction_id() -> str | None:
    context = _CONTEXT_VAR.get(None)
    return None if context is None else context.transaction_id


def transact_data(
    *,
    allow_nested: bool,
    commit: Callable[[str], None],
    rollback: Callable[[str], None],
    session_id: str,
    start: Callable[[], str],
    table_identifiers: DataTransactionTableIdentifiers | None,
) -> AbstractContextManager[None]:
    def create_context(
        transaction_id: str,
        /,
        *,
        previous_context: DataTransactionContext | None,
        session_id: str,
    ) -> DataTransactionContext:
        if (
            previous_context is not None
            and previous_context.table_identifiers is not None
        ):
            if table_identifiers is None:
                raise RuntimeError(
                    f"Cannot start a transaction locking all tables inside another transaction locking a subset of tables: {set(previous_context.table_identifiers)}.",
                )
            if not (table_identifiers < previous_context.table_identifiers):
                raise RuntimeError(
                    f"Cannot start a transaction locking tables {table_identifiers} inside another transaction locking tables {set(previous_context.table_identifiers)} which is not a superset.",
                )

        return DataTransactionContext(
            session_id=session_id,
            table_identifiers=table_identifiers,
            transaction_id=transaction_id,
        )

    return transact(
        allow_nested=allow_nested,
        commit=commit,
        context_var=_CONTEXT_VAR,
        create_context=create_context,
        rollback=rollback,
        session_id=session_id,
        start=start,
    )
