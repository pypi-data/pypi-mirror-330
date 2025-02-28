from enum import Enum
from typing import Any

from verse.core import DataModel
from verse.internal.storage_core import Index


class SearchFieldType(str, Enum):
    """Search field type."""

    STRING = "string"
    NUMBER = "number"
    BOOLEAN = "boolean"
    OBJECT = "object"
    ARRAY = "array"
    NULL = "null"


class SearchKey(DataModel):
    """Search key."""

    id: str
    """Content id."""

    pk: str | None = None
    """Optional partition key."""


class SearchProperties(DataModel):
    """Search properties."""

    etag: str | None = None
    """Content ETag."""

    score: float | None = None
    """Match score."""


class SearchItem(DataModel):
    """Search item."""

    key: SearchKey
    """Search key."""

    value: dict[str, Any] | None = None
    """Content value."""

    properties: SearchProperties | None = None
    """Search properties."""


class SearchList(DataModel):
    """Search list."""

    items: list[SearchItem]
    """List of search items."""


class SearchCollectionConfig(DataModel):
    """Search collection config."""

    indexes: list[Index] | None = None
    """Indexes."""

    nconfig: dict | None = None
    """Native config parameters."""


class SearchQueryConfig(DataModel):
    """Query config."""

    paging: bool | None = False
    """A value indicating whether the results should be paged."""

    page_size: int | None = None
    """Page size."""
