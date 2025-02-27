from mitm_tooling.representation import Header
from mitm_tooling.transformation.superset.definition_bundles import SupersetVisualizationBundle, \
    SupersetDatasourceBundle
from mitm_tooling.transformation.superset.factories.mitm_specific.maed_charts import mk_maed_charts
from mitm_tooling.transformation.superset.factories.mitm_specific.maed_dashboards import mk_maed_dashboard


def mk_maed_visualization(header: Header,
                          superset_datasource_bundle: SupersetDatasourceBundle) -> SupersetVisualizationBundle:
    ds_ids = superset_datasource_bundle.placeholder_dataset_identifiers

    charts = mk_maed_charts(header, superset_datasource_bundle)
    dashboard = mk_maed_dashboard(header, superset_datasource_bundle)
    return SupersetVisualizationBundle(charts=charts, dashboards=[dashboard])
