from pydantic import AnyUrl, UUID4

from .utils import mk_uuid
from ..common import name_plus_uuid
from ..definitions import SupersetDatabaseDef


def mk_database(name: str,
                sqlalchemy_uri: AnyUrl,
                uuid: UUID4 | None = None,
                uniquify_name: bool = False) -> SupersetDatabaseDef:
    uuid = uuid or mk_uuid()
    if uniquify_name:
        name = name_plus_uuid(name, uuid)
    return SupersetDatabaseDef(database_name=name, sqlalchemy_uri=sqlalchemy_uri, uuid=uuid)
