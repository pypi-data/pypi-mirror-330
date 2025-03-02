from __future__ import annotations

from collections.abc import Iterable
from typing import Any, Mapping, Literal, TypeAlias

from msgspec import Struct, msgpack
from msgspec import field as struct_field

__all__ = "Entry", "VariantManifest", "CacheIndex", "ApiIndex", "Cache", "MutableCache"

Cache: TypeAlias = Mapping[str, "Entry"]
MutableCache: TypeAlias = dict[str, "Entry"]

encoder = msgpack.Encoder()


class BaseIndex(Struct):
    name: str
    favicon_url: str | None

    def to_bytes(self) -> bytes:
        return encoder.encode(self)


class ApiIndex(BaseIndex, tag="api-index"):
    url: str
    options: dict[str, Any]
    version: Literal["2.1"] = "2.1"

class CacheIndex(BaseIndex, tag="cache-index"):
    cache: Cache
    version: Literal["2.1"] = "2.1"


class VariantManifest(Struct, tag="variant-manifest"):
    variants: Iterable[str]
    version: Literal["2.1"] = "2.1"


class Entry(Struct):
    text: str
    url: str
    options: dict[str, Any] = struct_field(default_factory=dict)

class ApiRequest(Struct):
    query: str
    options: dict[str, Any]
    version: Literal["2.1"] = "2.1"