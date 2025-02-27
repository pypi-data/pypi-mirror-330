import uuid

import pydantic


def mk_uuid() -> pydantic.UUID4:
    return uuid.uuid4()
