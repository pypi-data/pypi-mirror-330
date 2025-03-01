from typing import Literal, TypeVar

_ErrorType = type[KeyError] | type[RuntimeError]


_T = TypeVar("_T")


def _check_named_object_defined(
    object_value: _T | None,
    object_type: str,
    object_name: str,
    /,
    *,
    error_type: _ErrorType,
) -> _T:
    if object_value is None:
        raise error_type(f"No {object_type} named `{object_name}`.")

    return object_value


# Revisit the need for this function once https://github.com/graphql/graphql-wg/pull/772 is supported by Spring for GraphQL and ariadne-codegen.
def check_named_object_defined(
    object_value: _T | None,
    # The `Literal` provides autocomplete and prevent typos, feel free to add new strings as needed.
    object_type: Literal[
        "column",
        "cube",
        "dimension",
        "hierarchy",
        "level",
        "measure",
        "query cube",
        "table",
    ],
    object_name: str,
    /,
    *,
    error_type: _ErrorType = RuntimeError,
) -> _T:
    """Check that *object_value* is not ``None`` and return it.

    When ``object_value`` is ``None``, this function raises an informative error message mentioning both **object_type** and **object_name**.
    It provides a better UX than ``assert object_value is not None`` (and also raises even when ``assert``s are disabled).
    """
    return _check_named_object_defined(
        object_value,
        object_type,
        object_name,
        error_type=error_type,
    )
