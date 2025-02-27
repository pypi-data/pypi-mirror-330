from mitm_tooling.definition import MITM
from mitm_tooling.representation import Header
from mitm_tooling.transformation.superset.definition_bundles import SupersetDatasourceBundle, \
    SupersetVisualizationBundle, SupersetMitMDatasetBundle
from mitm_tooling.transformation.superset.from_intermediate import header_into_superset_mitm_dataset
from pydantic import AnyUrl
from typing import Callable

from . import mitm_specific
from .common import SupersetDBConnectionInfo
from .from_intermediate import header_into_superset_datasource_bundle
from ...representation.sql_representation import SQL_REPRESENTATION_DEFAULT_SCHEMA, SchemaName

mitm_specific_visualization_factories: dict[
    MITM, Callable[[Header, SupersetDatasourceBundle], SupersetVisualizationBundle]] = {
    MITM.MAED: mitm_specific.mk_maed_visualization,
}


def mk_superset_datasource_import(header: Header, sql_alchemy_uri: AnyUrl, explicit_db_name: str | None = None,
                                  schema_name: SchemaName = SQL_REPRESENTATION_DEFAULT_SCHEMA) -> SupersetDatasourceBundle:
    db_conn_info = SupersetDBConnectionInfo(sql_alchemy_uri=sql_alchemy_uri, explicit_db_name=explicit_db_name,
                                            schema_name=schema_name)
    return header_into_superset_datasource_bundle(header, db_conn_info)


def mk_superset_mitm_dataset_import(header: Header, sql_alchemy_uri: AnyUrl, dataset_name: str,
                                    explicit_db_name: str | None = None,
                                    schema_name: SchemaName = SQL_REPRESENTATION_DEFAULT_SCHEMA) -> SupersetMitMDatasetBundle:
    db_conn_info = SupersetDBConnectionInfo(sql_alchemy_uri=sql_alchemy_uri, explicit_db_name=explicit_db_name,
                                            schema_name=schema_name)
    return header_into_superset_mitm_dataset(header, db_conn_info, dataset_name=dataset_name)


def mk_superset_visualization_import(header: Header,
                                     superset_datasource_bundle: SupersetDatasourceBundle) -> SupersetVisualizationBundle:
    return mitm_specific_visualization_factories[header.mitm](header, superset_datasource_bundle)
