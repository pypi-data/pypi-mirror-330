from abc import abstractmethod
from collections import defaultdict
from datetime import UTC

from mitm_tooling.definition import MITM
from .charts import *
from .post_processing import *


class MetadataType(StrEnum):
    Database = 'Database'
    SqlaTable = 'SqlaTable'
    Slice = 'Slice'
    Chart = 'Chart'
    Dashboard = 'Dashboard'
    Asset = 'Asset'
    MitMDataset = 'MitMDataset'


class SupersetDefFile(BaseSupersetDefinition, ABC):

    @property
    @abstractmethod
    def filename(self) -> str:
        pass


class SupersetDefFolder(BaseSupersetDefinition, ABC):

    @property
    @abstractmethod
    def folder_dict(self) -> dict[str, Any]:
        pass


class SupersetMetadataDef(SupersetDefFile):
    version: str = '1.0.0'
    type: MetadataType = MetadataType.SqlaTable
    timestamp: StrDatetime = pydantic.Field(default_factory=lambda: datetime.now(UTC))

    @property
    def filename(self) -> str:
        return 'metadata'


class SupersetDatabaseDef(SupersetDefFile):
    database_name: str
    sqlalchemy_uri: StrUrl
    uuid: StrUUID
    # verbose_name : str | None = None
    cache_timeout: str | None = None
    expose_in_sqllab: bool = True
    allow_run_async: bool = False
    allow_ctas: bool = False
    allow_cvas: bool = False
    allow_dml: bool = False
    allow_file_upload: bool = False
    extra: dict[str, Any] = pydantic.Field(default_factory=lambda: {
        'allows_virtual_table_explore': True
    })
    impersonate_user: bool = False
    version: str = '1.0.0'
    ssh_tunnel: None = None

    @property
    def filename(self):
        return self.database_name


class SupersetDatasetDef(SupersetDefFile):
    table_name: str
    schema_name: str = pydantic.Field(alias='schema')
    uuid: StrUUID
    database_uuid: StrUUID
    main_dttm_col: str | None = None
    description: str | None = None
    default_endpoint: str | None = None
    offset: int = 0
    cache_timeout: str | None = None
    catalog: str | None = None
    sql: str | None = None
    params: Any = None
    template_params: Any = None
    filter_select_enabled: bool = True
    fetch_values_predicate: str | None = None
    extra: dict[str, Any] = pydantic.Field(default_factory=dict)
    normalize_columns: bool = False
    always_filter_main_dttm: bool = False
    metrics: list[SupersetMetric] = pydantic.Field(default_factory=list)
    columns: list[SupersetColumn] = pydantic.Field(default_factory=list)
    version: str = '1.0.0'

    @property
    def filename(self):
        return self.table_name


class SupersetChartDef(SupersetDefFile):
    uuid: StrUUID
    slice_name: str
    viz_type: SupersetVizType
    dataset_uuid: StrUUID
    description: str | None = None
    certified_by: str | None = None
    certification_details: str | None = None
    params: ChartParams | dict[str, Any] = pydantic.Field(default_factory=dict)
    query_context: Annotated[pydantic.Json | QueryContext | None, pydantic.PlainSerializer(
        lambda x: x.model_dump_json(by_alias=True, exclude_none=True) if isinstance(x, pydantic.BaseModel) else x,
        return_type=pydantic.Json), pydantic.Field(default=None)]
    cache_timeout: int | None = None
    version: str = '1.0.0'
    is_managed_externally: bool = False
    external_url: StrUrl | None = None

    @property
    def filename(self) -> str:
        return f'{self.slice_name}_{self.dataset_uuid}'


class SupersetDashboardDef(SupersetDefFile):
    uuid: StrUUID
    dashboard_title: str
    description: str | None = None
    css: str | None = None
    slug: str | None = None
    position: dict[str, Any] = pydantic.Field(default_factory=dict)
    metadata: dict[str, Any] = pydantic.Field(default_factory=dict)
    is_managed_externally: bool | None = False
    external_url: StrUrl | None = None
    certified_by: str | None = None
    certification_details: str | None = None
    published: bool | None = False
    version: str = '1.0.0'

    @property
    def filename(self) -> str:
        return f'{self.dashboard_title}_{self.uuid}'


class SupersetMitMDatasetDef(SupersetDefFile):
    uuid: StrUUID
    dataset_name: str
    mitm: MITM
    database_uuid: StrUUID
    version: str = '1.0.0'

    @property
    def filename(self) -> str:
        return self.dataset_name


class SupersetAssetsDef(SupersetDefFolder):
    databases: list[SupersetDatabaseDef] | None = None
    datasets: list[SupersetDatasetDef] | None = None
    charts: list[SupersetChartDef] | None = None
    dashboards: list[SupersetDashboardDef] | None = None
    metadata: SupersetMetadataDef = pydantic.Field(default_factory=SupersetMetadataDef)

    @property
    def folder_dict(self) -> dict[str, Any]:
        folder_dict = {'.': self.metadata}
        dbs = {}
        if self.databases:
            dbs |= {db.uuid: db.database_name for db in self.databases}
            folder_dict['databases'] = [db for db in self.databases]
        if self.datasets:
            db_dss = defaultdict(list)
            for ds in self.datasets:
                db_dss[dbs[ds.database_uuid]].append(ds)
            folder_dict['datasets'] = db_dss
        if self.charts:
            folder_dict['charts'] = self.charts
        return {'my_import': folder_dict}


class ExtendedSupersetAssetsDef(SupersetDefFolder):
    mitm_datasets: list[SupersetMitMDatasetDef] | None
    base_assets: SupersetAssetsDef | None

    @property
    def folder_dict(self) -> dict[str, Any]:
        asset_folder_dict = self.base_assets.folder_dict if self.base_assets else {'my_import': {}}
        dbs = {}
        if self.base_assets.databases:
            dbs = {db.uuid: db.database_name for db in self.base_assets.databases}
        if self.mitm_datasets:
            mitm_dss = defaultdict(list)
            for mitm_ds in self.mitm_datasets:
                mitm_dss[dbs[mitm_ds.database_uuid]].append(mitm_ds)
            asset_folder_dict['my_import']['mitm_datasets'] = mitm_dss
        return asset_folder_dict
