import pydantic
import sqlalchemy as sa

from mitm_tooling.data_types import MITMDataType
from mitm_tooling.extraction.sql.data_models import TableMetaInfo
from mitm_tooling.transformation.superset.definitions import SupersetDatasetDef
from .core import mk_column, mk_metric
from .utils import mk_uuid
from ..definitions import SupersetAggregate


def mk_dataset(tm: TableMetaInfo, database_uuid: pydantic.UUID4, dialect: sa.Dialect | None = None,
               uuid: pydantic.UUID4 | None = None) -> SupersetDatasetDef:
    cols = []
    metrics = [mk_metric('*', SupersetAggregate.COUNT)]
    for c in tm.columns:
        dt = tm.column_properties[c].mitm_data_type
        cols.append(
            mk_column(c, dt, dialect=dialect),
        )
        if dt in {MITMDataType.Numeric, MITMDataType.Integer}:
            metrics.extend((
                mk_metric(c, SupersetAggregate.AVG),
                mk_metric(c, SupersetAggregate.SUM),
            ))

    return SupersetDatasetDef(table_name=tm.name, schema=tm.schema_name, uuid=uuid or mk_uuid(),
                              database_uuid=database_uuid, columns=cols, metrics=metrics)
