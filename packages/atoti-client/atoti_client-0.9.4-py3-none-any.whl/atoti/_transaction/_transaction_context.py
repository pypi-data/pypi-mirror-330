from pydantic.dataclasses import dataclass

from .._pydantic import PYDANTIC_CONFIG as _PYDANTIC_CONFIG


@dataclass(config=_PYDANTIC_CONFIG, frozen=True, kw_only=True)
# Not `@final` because inherited by `DataTransactionContext` and `DataModelTransactionContext`.
class TransactionContext:  # pylint: disable=final-class
    session_id: str
    transaction_id: str
