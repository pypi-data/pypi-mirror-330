from verse.core.exceptions import BadRequestError
from verse.internal.storage_core import StoreOperationParser

from ._models import SearchCollectionConfig


def get_collection_config(op_parser: StoreOperationParser):
    config = op_parser.get_config()
    if config is None:
        return None
    if isinstance(config, dict):
        return SearchCollectionConfig.from_dict(config)
    if isinstance(config, SearchCollectionConfig):
        return config
    raise BadRequestError("Collection config format error")
