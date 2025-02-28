from pydantic.version import VERSION as PYDANTIC_VERSION

PYDANTIC_V2 = PYDANTIC_VERSION.startswith("2.")

if PYDANTIC_V2:
    from pydantic.v1 import BaseModel  # type: ignore[assignment]
    from pydantic.v1 import Field  # type: ignore[assignment]
    from pydantic.v1 import validator  # type: ignore[assignment]
else:
    from pydantic import BaseModel  # type: ignore[assignment]
    from pydantic import Field  # type: ignore[assignment]
    from pydantic import validator  # type: ignore[assignment]
