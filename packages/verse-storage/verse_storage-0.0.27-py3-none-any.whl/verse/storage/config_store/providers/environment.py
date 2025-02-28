"""
Config Store on Environment variables.
"""

__all__ = ["Environment"]

import os
from typing import Any

from verse.core import Context, Operation, Response
from verse.core.exceptions import BadRequestError, NotFoundError
from verse.internal.storage_core import StoreOperation, StoreProvider

from .._constants import DEFAULT_LABEL
from .._helper import normalize_label
from .._models import ConfigItem, ConfigKey


class Environment(StoreProvider):
    def __init__(self, **kwargs):
        """Initialize."""
        pass

    def __setup__(self, context: Context | None = None) -> None:
        pass

    def __run__(
        self,
        operation: Operation | None = None,
        context: Context | None = None,
        **kwargs,
    ) -> Any:
        self.__setup__(context=context)
        op_parser = self.get_op_parser(operation)
        # GET value
        if op_parser.op_equals(StoreOperation.GET):
            id = op_parser.get_id_as_str()
            label = normalize_label(op_parser.get_label())
            if label != DEFAULT_LABEL:
                raise BadRequestError(
                    "Custom label in not support in environment"
                )
            val = os.environ.get(id)
            if val is None:
                raise NotFoundError
            result = ConfigItem(
                key=ConfigKey(id=id, label=label),
                value=val,
            )
        # PUT
        elif op_parser.op_equals(StoreOperation.PUT):
            id = op_parser.get_id_as_str()
            label = normalize_label(op_parser.get_label())
            value = str(op_parser.get_value())
            if label != DEFAULT_LABEL:
                raise BadRequestError(
                    "Custom label in not support in environment"
                )
            os.environ[id] = value
            result = ConfigItem(key=ConfigKey(id=id, label=label))
        # DELETE
        elif op_parser.op_equals(StoreOperation.DELETE):
            id = op_parser.get_id_as_str()
            label = normalize_label(op_parser.get_label())
            if label != DEFAULT_LABEL:
                raise BadRequestError(
                    "Custom label in not support in environment"
                )
            try:
                os.environ.pop(id)
            except KeyError:
                raise NotFoundError
            result = None
        # CLOSE
        elif op_parser.op_equals(StoreOperation.CLOSE):
            result = None
        else:
            return super().__run__(
                operation,
                context,
                **kwargs,
            )
        return Response(result=result)
