from mitm_tooling.representation import Header

from .common import SupersetDBConnectionInfo
from .definition_bundles import SupersetDatasourceBundle, SupersetMitMDatasetBundle
from ...definition import MITM


def header_into_superset_datasource_bundle(header: Header,
                                           db_conn_info: SupersetDBConnectionInfo) -> SupersetDatasourceBundle:
    from ..sql.from_intermediate import header_into_db_meta
    from .from_sql import db_meta_into_superset_datasource_bundle
    db_meta = header_into_db_meta(header)
    return db_meta_into_superset_datasource_bundle(db_meta, db_conn_info)


def header_into_superset_mitm_dataset(header: Header,
                                      db_conn_info: SupersetDBConnectionInfo,
                                      dataset_name: str) -> SupersetMitMDatasetBundle:
    from ..sql.from_intermediate import header_into_db_meta
    from .from_sql import db_meta_into_mitm_dataset_bundle
    db_meta = header_into_db_meta(header)
    return db_meta_into_mitm_dataset_bundle(db_meta, db_conn_info, dataset_name, header.mitm)
