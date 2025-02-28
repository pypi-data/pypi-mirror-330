"""
Elastic Search.
"""

from __future__ import annotations

import re

__all__ = ["Elasticsearch"]


from typing import Any

from elasticsearch import AsyncElasticsearch
from elasticsearch import Elasticsearch as SyncElasticsearch

from verse.core import Context, Response
from verse.core.exceptions import BadRequestError
from verse.core.models import Expression
from verse.internal.storage_core import (
    ArrayIndex,
    AscIndex,
    CompositeIndex,
    DescIndex,
    ExcludeIndex,
    FieldIndex,
    GeospatialFieldType,
    GeospatialIndex,
    HashIndex,
    Index,
    ItemProcessor,
    ParameterParser,
    RangeIndex,
    SparseVectorIndex,
    StoreProvider,
    TextIndex,
    TextSimilarityAlgorithm,
    VectorIndex,
    VectorIndexMetric,
    VectorIndexStructure,
)

from .._models import SearchCollectionConfig
from .._operation_parser import OperationParser


class Elasticsearch(StoreProvider):
    hosts: str | dict[str, str | int]
    cloud_id: str | None
    api_key: str | list[str] | None
    basic_auth: str | list[str] | None
    bearer_auth: str | None
    opaque_id: str | None
    http_auth: str | Any | None

    headers: dict[str, str] | None
    verify_certs: bool | None
    ca_certs: str | None
    client_cert: str | None
    client_key: str | None
    ssl_assert_hostname: str | None
    ssl_assert_fingerprint: str | None
    ssl_version: int | None

    index: str | None
    id_map_field: str | dict | None
    pk_map_field: str | dict | None
    nparams: dict[str, Any]

    _client: Any
    _aclient: Any

    _op_parser: OperationParser
    _collection_cache: dict[str, ElasticsearchCollection]

    def __init__(
        self,
        hosts: str | dict[str, str | int],
        cloud_id: str | None = None,
        api_key: str | list[str] | None = None,
        basic_auth: str | list[str] | None = None,
        bearer_auth: str | None = None,
        opaque_id: str | None = None,
        http_auth: str | list[str] | Any | None = None,
        headers: dict[str, str] | None = None,
        verify_certs: bool | None = None,
        ca_certs: str | None = None,
        client_cert: str | None = None,
        client_key: str | None = None,
        ssl_assert_hostname: str | None = None,
        ssl_assert_fingerprint: str | None = None,
        ssl_version: int | None = None,
        index: str | None = None,
        id_map_field: str | dict | None = "id",
        pk_map_field: str | dict | None = None,
        nparams: dict[str, Any] = dict(),
        **kwargs,
    ):
        """Initialize.

        Args:
            hosts:
                Elasticsearch hosts.
            cloud_id:
                Elasticsearch cloud id.
            api_key:
                Elasticsearch api key.
            basic_auth:
                Elasticsearch basic auth.
            bearer_auth:
                Elasticsearch bearer auth.
            opaque_id:
                Elasticsearch opaque id.
            http_auth:
                Elasticsearch http auth.
            headers:
                Elasticsearch http headers.
            verify_certs:
                Elasticsearch verify certs.
            ca_certs:
                Elasticsearch ca certs.
            client_cert:
                Elasticsearch client cert.
            client_key:
                Elasticsearch client key.
            ssl_assert_hostname:
                Elasticsearch ssl assert hostname.
            ssl_assert_fingerprint:
                Elasticsearch ssl assert fingerprint.
            ssl_version:
                Elasticsearch ssl version.
            index:
                Elasticsearch index mapped to
                search store collection.
            id_map_field:
                Field in the content to map into id.
                To specify for multiple collections, use a dictionary
                where the key is the collection name and the value
                is the field.
            pk_map_field:
                Field in the content to map into pk.
                To specify for multiple collections, use a dictionary
                where the key is the collection name and the value
                is the field.
            nparams:
                Native parameters to Elasticsearch client.
        """
        self.hosts = hosts
        self.cloud_id = cloud_id
        self.api_key = api_key
        self.basic_auth = basic_auth
        self.bearer_auth = bearer_auth
        self.opaque_id = opaque_id
        self.http_auth = http_auth
        self.headers = headers
        self.verify_certs = verify_certs
        self.ca_certs = ca_certs
        self.client_cert = client_cert
        self.client_key = client_key
        self.ssl_assert_hostname = ssl_assert_hostname
        self.ssl_assert_fingerprint = ssl_assert_fingerprint
        self.ssl_version = ssl_version

        self.index = index
        self.id_map_field = id_map_field
        self.pk_map_field = pk_map_field
        self.nparams = nparams

        self._client = None
        self._aclient = None
        self._collection_cache = dict()

    @property
    def client(self) -> SyncElasticsearch:
        if self._client is None:
            self._client = SyncElasticsearch(**self._get_client_params())
        return self._client

    @property
    def aclient(self) -> AsyncElasticsearch:
        if self._aclient is None:
            self._client = AsyncElasticsearch(**self._get_client_params())
        return self._client

    def __setup__(self, context: Context | None = None) -> None:
        _ = self.client

    async def __asetup__(self, context: Context | None = None) -> None:
        _ = self.aclient

    def _get_client_params(self) -> dict:
        def _add_if_not_none(key, value):
            return {key: value} if value is not None else {}

        def _convert_if_list(value):
            return tuple(value) if isinstance(value, list) else value

        args = {
            "hosts": self.hosts,
            **_add_if_not_none("cloud_id", self.cloud_id),
            **_add_if_not_none("api_key", _convert_if_list(self.api_key)),
            **_add_if_not_none(
                "basic_auth", _convert_if_list(self.basic_auth)
            ),
            **_add_if_not_none("bearer_auth", self.bearer_auth),
            **_add_if_not_none("opaque_id", self.opaque_id),
            **_add_if_not_none("http_auth", self.http_auth),
            **_add_if_not_none("headers", self.headers),
            **_add_if_not_none("verify_certs", self.verify_certs),
            **_add_if_not_none("ca_certs", self.ca_certs),
            **_add_if_not_none("client_cert", self.client_cert),
            **_add_if_not_none("client_key", self.client_key),
            **_add_if_not_none(
                "ssl_assert_hostname", self.ssl_assert_hostname
            ),
            **_add_if_not_none(
                "ssl_assert_fingerprint", self.ssl_assert_fingerprint
            ),
            **_add_if_not_none("ssl_version", self.ssl_version),
        }

        if self.nparams is not None:
            args.update(self.nparams)

        return args

    def _get_collection_name(
        self,
        collection_name: str | None,
    ) -> str:
        collection_name = (
            collection_name or self.index or self.get_component().collection
        )
        if not collection_name:
            raise BadRequestError("Collection name must be specified")
        return collection_name

    def _get_collection(
        self,
        collection_name: str,
    ) -> ElasticsearchCollection:
        if collection_name in self._collection_cache:
            return self._collection_cache[collection_name]
        id_map_field = ParameterParser.get_collection_parameter(
            self.id_map_field or self.get_component().id_map_field,
            collection_name,
        )
        pk_map_field = ParameterParser.get_collection_parameter(
            self.pk_map_field or self.get_component().pk_map_field,
            collection_name,
        )
        collection = ElasticsearchCollection(
            id_map_field,
            pk_map_field,
            collection_name,
        )
        self._collection_cache[collection_name] = collection
        return collection

    def create_collection(
        self,
        collection: str | None = None,
        config: dict | SearchCollectionConfig | None = None,
        where: str | Expression | None = None,
        **kwargs: Any,
    ) -> Response[None]:
        pass


class OperationConverter:
    processor: ItemProcessor
    collection: str

    def __init__(self, processor: ItemProcessor, collection: str) -> None:
        self.processor = processor
        self.collection = collection

    def convert_create_collection(
        self,
        collection: str,
        config: SearchCollectionConfig | None,
    ) -> dict:
        args: dict = {"index": collection}
        if config and config.nconfig:
            args.update(config.nconfig)
        return args

    def _convert_index(self, index: Index) -> dict:
        pass


class ResultConverter:
    processor: ItemProcessor
    collection: str

    def __init__(self, processor: ItemProcessor, collection: str) -> None:
        self.processor = processor
        self.collection = collection


class IndexHelper:
    @staticmethod
    def add_index(mappings: dict, index: Index) -> None:
        field, config = IndexHelper.convert_index_to_config(index)
        if not field:
            return
        path = re.sub(r"\[\d+\]", "", field)
        path_parts = path.split(".")
        current = mappings
        for part in path_parts[:-1]:
            is_array = "[]" in part
            part = part.replace("[]", "")
            if "properties" not in current:
                current["properties"] = {}
            if part not in current["properties"]:
                current["properties"][part] = (
                    {"type": "nested"} if is_array else {}
                )
            current = current["properties"][part]
        if "properties" not in current:
            current["properties"] = {}
        current["properties"][path_parts[-1]] = config

    @staticmethod
    def remove_index(mappings: dict, index: Index) -> None:
        field, config = IndexHelper.convert_index_to_config(index)
        if not field:
            return
        path = re.sub(r"\[\d+\]", "", field)
        path_parts = path.split(".")
        current = mappings
        stack = []
        for part in path_parts[:-1]:
            if (
                "properties" not in current
                or part not in current["properties"]
            ):
                return
            stack.append((current, part))
            current = current["properties"][part]

        field_name = path_parts[-1]
        if "properties" in current and field_name in current["properties"]:
            del current["properties"][field_name]

        while stack:
            parent, part = stack.pop()
            if "properties" in parent[part] and not parent[part]["properties"]:
                del parent[part]
            else:
                break

    @staticmethod
    def convert_index_to_config(index: Index) -> tuple[str | None, dict]:
        field = None
        config: dict = {}
        if isinstance(
            index,
            (
                RangeIndex,
                HashIndex,
                FieldIndex,
                ArrayIndex,
                AscIndex,
                DescIndex,
            ),
        ):
            field = index.field
            config["type"] = index.field_type
        elif isinstance(index, TextIndex):
            field = index.field
            if index.variant == "match_only_text":
                config["type"] = "match_only_text"
            else:
                config["type"] = "text"
            if index.similarity is not None:
                similarity_map = {
                    TextSimilarityAlgorithm.BM25: "BM25",
                    TextSimilarityAlgorithm.BOOLEAN: "boolean",
                }
                config["similarity"] = similarity_map[index.similarity]
        elif isinstance(index, VectorIndex):
            field = index.field
            metric_map = {
                VectorIndexMetric.DOT_PRODUCT: "dot_product",
                VectorIndexMetric.EUCLIDEAN: "l2_norm",
                VectorIndexMetric.COSINE: "cosine",
                VectorIndexMetric.MAX_INNER_PRODUCT: "max_inner_product",
            }
            config["type"] = "dense_vector"
            config["dims"] = index.dimension
            config["similarity"] = metric_map[index.metric]
            if index.field_type is not None:
                config["element_type"] = index.field_type
            if index.structure is not None:
                structure_map = {
                    VectorIndexStructure.FLAT: "flat",
                    VectorIndexStructure.INT8_FLAT: "int8_flat",
                    VectorIndexStructure.INT4_FLAT: "int4_flat",
                    VectorIndexStructure.BQ_FLAT: "bbq_flat",
                    VectorIndexStructure.HNSW: "hnsw",
                    VectorIndexStructure.INT8_HNSW: "int8_hnsw",
                    VectorIndexStructure.INT4_HNSW: "int4_hnsw",
                    VectorIndexStructure.BQ_HNSW: "bq_hnsw",
                }
                index_options: dict = {"type": structure_map[index.structure]}
                if index.m is not None:
                    index_options["m"] = index.m
                if index.confidence_interval is not None:
                    index_options["confidence_interval"] = (
                        index.confidence_interval
                    )
                if index.ef_construction is not None:
                    index_options["ef_construction"] = index.ef_construction
                config["index_options"] = index_options
        elif isinstance(index, SparseVectorIndex):
            field = index.field
            config["type"] = "sparse_vector"
        elif isinstance(index, GeospatialIndex):
            field = index.field
            field_type_map = {
                GeospatialFieldType.POINT.value: "geo_point",
                GeospatialFieldType.SHAPE.value: "geo_shape",
            }
            if index.field_type:
                config["type"] = field_type_map[index.field_type]
            else:
                config["type"] = "geo_point"
        elif isinstance(index, CompositeIndex):
            pass
        elif isinstance(index, ExcludeIndex):
            field = index.field
            config = {"index": False}
        if isinstance(index.nconfig, dict):
            config.update(index.nconfig)
        return field, config


class ElasticsearchCollection:
    op_converter: OperationConverter
    result_converter: ResultConverter

    def __init__(
        self,
        id_map_field: str | None,
        pk_map_field: str | None,
        collection: str,
    ):
        self.processor = ItemProcessor(
            id_map_field=id_map_field,
            pk_map_field=pk_map_field,
        )
        self.op_converter = OperationConverter(
            processor=self.processor, collection=collection
        )
        self.result_converter = ResultConverter(
            processor=self.processor, collection=collection
        )
