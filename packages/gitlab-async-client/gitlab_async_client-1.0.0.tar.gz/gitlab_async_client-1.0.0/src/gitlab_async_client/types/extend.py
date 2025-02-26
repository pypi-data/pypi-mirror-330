from typing import Any

import arrow

from pydantic import (
    GetCoreSchemaHandler,
)
from pydantic_core import core_schema


class ArrowPydanticV2(arrow.Arrow):
    @classmethod
    def __get_pydantic_core_schema__(
        cls,
        _source_type: Any,
        _handler: GetCoreSchemaHandler,
    ) -> core_schema.CoreSchema:
        def validate_by_arrow(value) -> arrow.Arrow:
            try:
                return arrow.get(value)
            except Exception:
                raise ValueError('Not a valid value for arrow')

        def arrow_serialization(value: Any) -> str | arrow.Arrow:
            return value

        return core_schema.no_info_after_validator_function(
            function=validate_by_arrow,
            schema=core_schema.str_schema(),
            serialization=core_schema.wrap_serializer_function_ser_schema(
                arrow_serialization, info_arg=True
            ),
        )
