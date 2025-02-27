from pydantic.v1 import UUID4

from mitm_tooling.definition import MITM
from mitm_tooling.transformation.superset.definitions import SupersetMitMDatasetDef
from mitm_tooling.transformation.superset.factories.utils import mk_uuid


def mk_mitm_dataset(name: str, mitm: MITM, database_uuid: UUID4, uuid: UUID4 | None = None) -> SupersetMitMDatasetDef:
    return SupersetMitMDatasetDef(
        dataset_name=name,
        mitm=mitm,
        database_uuid=database_uuid,
        uuid=uuid or mk_uuid()
    )
