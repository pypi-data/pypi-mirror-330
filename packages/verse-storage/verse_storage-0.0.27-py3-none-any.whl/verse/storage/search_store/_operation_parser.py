from verse.core.exceptions import BadRequestError

from ._models import SearchCollectionConfig


class OperationParser:
    def get_collection_config(
        self,
        config: dict | SearchCollectionConfig | None,
    ) -> SearchCollectionConfig | None:
        if config is None:
            return None
        if isinstance(config, dict):
            return SearchCollectionConfig.from_dict(config)
        if isinstance(config, SearchCollectionConfig):
            return config
        raise BadRequestError("Collection config format error")
