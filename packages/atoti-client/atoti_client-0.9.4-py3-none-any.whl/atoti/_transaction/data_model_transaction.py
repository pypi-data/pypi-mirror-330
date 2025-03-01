from __future__ import annotations

from collections.abc import Callable
from contextlib import AbstractContextManager
from contextvars import ContextVar
from typing import final

from pydantic.dataclasses import dataclass

from .._pydantic import PYDANTIC_CONFIG as _PYDANTIC_CONFIG
from ._transact import transact
from ._transaction_context import TransactionContext


@final
@dataclass(config=_PYDANTIC_CONFIG, frozen=True, kw_only=True)
class DataModelTransactionContext(TransactionContext): ...


_CONTEXT_VAR: ContextVar[DataModelTransactionContext] = ContextVar(
    "atoti_data_model_transaction",
)


def data_model_transaction_id() -> str | None:
    context = _CONTEXT_VAR.get(None)
    return None if context is None else context.transaction_id


def transact_data_model(
    *,
    allow_nested: bool,
    commit: Callable[..., None],
    session_id: str,
) -> AbstractContextManager[None]:
    def start() -> str:
        # In the future, Atoti Server will be aware of the data model transaction and provide its ID to the client.
        return "unused"

    def rollback(
        transaction_id: str,
    ) -> None:
        # Rollback of data model transactions is not supported yet.
        ...

    def create_context(
        transaction_id: str,
        /,
        *,
        previous_context: DataModelTransactionContext | None,  # noqa: ARG001
        session_id: str,
    ) -> DataModelTransactionContext:
        return DataModelTransactionContext(
            session_id=session_id,
            transaction_id=transaction_id,
        )

    return transact(
        allow_nested=allow_nested,
        commit=lambda _: commit(),
        context_var=_CONTEXT_VAR,
        create_context=create_context,
        rollback=rollback,
        session_id=session_id,
        start=start,
    )
