from typing import Any, Annotated

import msgspec


class JsonSchema(msgspec.Struct):
    schema: Annotated[
        dict[str, Any], msgspec.Meta(description="Stores the JSON schema object.")
    ]
