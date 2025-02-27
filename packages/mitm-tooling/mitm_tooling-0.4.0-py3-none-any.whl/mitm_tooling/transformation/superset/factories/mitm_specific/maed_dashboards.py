from mitm_tooling.representation import Header
from mitm_tooling.transformation.superset.definition_bundles import SupersetDatasourceBundle
from mitm_tooling.transformation.superset.definitions import SupersetDashboardDef
from mitm_tooling.transformation.superset.factories.dashboard import mk_superset_dashboard
from mitm_tooling.transformation.superset.factories.mitm_specific.maed_charts import mk_maed_charts


def mk_maed_dashboard(header: Header, datasource_bundle: SupersetDatasourceBundle) -> SupersetDashboardDef:
    charts = mk_maed_charts(header, datasource_bundle)
    position = {}
    return mk_superset_dashboard('MAED Dashboard', position, description='A rudimentary dashboard to view MAED data.')
