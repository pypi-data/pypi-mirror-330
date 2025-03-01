from __future__ import annotations

import json
from collections.abc import Set as AbstractSet
from typing import Final, final
from urllib.parse import urlencode

import httpx

from .._activeviam_client import ActiveViamClient
from .._pydantic import get_type_adapter
from .content import ContentTree

_NAMESPACE = "activeviam/content"


@final
class ContentClient:
    def __init__(self, *, activeviam_client: ActiveViamClient) -> None:
        self._activeviam_client: Final = activeviam_client

    def _get_path(self, path: str, /) -> str:
        return f"{self._activeviam_client.get_endpoint_path(namespace=_NAMESPACE, route='files')}?{urlencode({'path': path})}"

    def get(self, path: str, /) -> ContentTree | None:
        path = self._get_path(path)
        response = self._activeviam_client.http_client.get(path)
        if response.status_code == httpx.codes.NOT_FOUND:
            return None
        response.raise_for_status()
        body = response.content
        return get_type_adapter(ContentTree).validate_json(body)  # type: ignore[arg-type] # pyright: ignore[reportArgumentType]

    def create(
        self,
        path: str,
        /,
        *,
        content: object,
        owners: AbstractSet[str],
        readers: AbstractSet[str],
    ) -> None:
        path = self._get_path(path)
        self._activeviam_client.http_client.put(
            path,
            json={
                "content": json.dumps(content),
                "owners": sorted(owners),
                "readers": sorted(readers),
                "overwrite": True,
                "recursive": True,
            },
        ).raise_for_status()

    def delete(self, path: str, /) -> None:
        path = self._get_path(path)
        self._activeviam_client.http_client.delete(path).raise_for_status()
