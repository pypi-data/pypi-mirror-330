from mitm_tooling.data_types import MITMDataType
from mitm_tooling.representation import SQLRepresentationSchema, Header, mk_sql_rep_schema
from mitm_tooling.utilities.python_utils import take_first
from ..charts import mk_avg_count_time_series_chart, mk_pie_chart, mk_time_series_bar_chart
from ..core import mk_adhoc_filter
from ...definition_bundles import SupersetDatasourceBundle
from ...definitions import SupersetChartDef, FilterOperator


def mk_maed_charts(header: Header, superset_datasource_bundle: SupersetDatasourceBundle,
                   sql_rep_schema: SQLRepresentationSchema | None = None) -> list[
    SupersetChartDef]:
    sql_rep_schema = sql_rep_schema or mk_sql_rep_schema(header)
    ds_ids = superset_datasource_bundle.placeholder_dataset_identifiers

    event_counts_ts = mk_time_series_bar_chart('Event Counts',
                                               ds_ids['observations'],
                                               'type',
                                               MITMDataType.Text,
                                               'time',
                                               groupby_cols=['object'],
                                               filters=[
                                                   mk_adhoc_filter('kind', FilterOperator.EQUALS, 'E')]
                                               )
    measurement_counts_ts = mk_time_series_bar_chart('Measurement Counts',
                                                     ds_ids['observations'],
                                                     'type',
                                                     MITMDataType.Text,
                                                     'time',
                                                     groupby_cols=['object'],
                                                     filters=[
                                                         mk_adhoc_filter('kind', FilterOperator.EQUALS, 'M')]
                                                     )
    objects_pie = mk_pie_chart('Objects', ds_ids['observations'], 'object', MITMDataType.Text)

    type_name, tbl = take_first(sql_rep_schema.type_tables['measurement'].items())  # TODO

    ts = mk_avg_count_time_series_chart(f'{type_name} Time Series', ds_ids[tbl.name], groupby_cols=['object'],
                                        filters=[mk_adhoc_filter('kind', FilterOperator.EQUALS, 'M')])
    return [event_counts_ts, measurement_counts_ts, objects_pie, ts]
