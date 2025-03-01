from __future__ import annotations

from collections.abc import Callable, Generator
from contextlib import contextmanager
from contextvars import ContextVar, Token
from typing import Generic, Protocol, TypeVar

from ._transaction_context import TransactionContext

_TransactionContextT = TypeVar("_TransactionContextT", bound=TransactionContext)


class CreateTransactionContext(Generic[_TransactionContextT], Protocol):
    def __call__(
        self,
        transaction_id: str,
        /,
        *,
        previous_context: _TransactionContextT | None,
        session_id: str,
    ) -> _TransactionContextT: ...


@contextmanager
def transact(
    *,
    allow_nested: bool,
    commit: Callable[[str], None],
    context_var: ContextVar[_TransactionContextT],
    create_context: CreateTransactionContext[_TransactionContextT],
    rollback: Callable[[str], None],
    session_id: str,
    start: Callable[[], str],
) -> Generator[None, None, None]:
    token: Token[_TransactionContextT] | None = None

    previous_context = context_var.get(None)

    if previous_context is not None:
        if previous_context.session_id != session_id:
            raise RuntimeError(
                "Cannot start this transaction inside a transaction started from another session.",
            )

        if not allow_nested:
            raise RuntimeError(
                "Cannot start this transaction inside another transaction since nesting is not allowed.",
            )

        transaction_id = previous_context.transaction_id
        is_nested_transaction = True

    else:
        transaction_id = start()
        is_nested_transaction = False

    context = create_context(
        transaction_id,
        session_id=session_id,
        previous_context=previous_context,
    )
    token = context_var.set(context)

    try:
        yield
    except:
        if is_nested_transaction:
            # Let the outer one handle this.
            ...
        else:
            transaction_id = context_var.get().transaction_id
            context_var.reset(token)
            rollback(transaction_id)

        raise
    else:
        if is_nested_transaction:
            # Let the outer one handle this.
            ...
        else:
            transaction_id = context_var.get().transaction_id
            context_var.reset(token)
            commit(transaction_id)
