from abc import ABC, abstractmethod
from typing import Any

import pydantic

from .definitions import SupersetDatabaseDef, SupersetMitMDatasetDef, \
    SupersetChartDef, SupersetDashboardDef, BaseSupersetDefinition, SupersetAssetsDef, SupersetDatasetDef, \
    ExtendedSupersetAssetsDef, SupersetDefFolder, DatasourceIdentifier
from .factories.assets import mk_assets, mk_extended_assets
from ...representation.sql.common import TableName


class SupersetAssetBundle(SupersetDefFolder, ABC):
    @abstractmethod
    def to_assets(self) -> SupersetAssetsDef | ExtendedSupersetAssetsDef:
        pass

    @property
    def folder_dict(self) -> dict[str, Any]:
        return self.to_assets().folder_dict


class SupersetDatasourceBundle(SupersetAssetBundle):
    database: SupersetDatabaseDef
    datasets: list[SupersetDatasetDef] = pydantic.Field(default_factory=list)

    @property
    def placeholder_dataset_identifiers(self) -> dict[TableName, DatasourceIdentifier]:
        return {ds.table_name: DatasourceIdentifier(dataset_uuid=ds.uuid) for ds in self.datasets}

    def to_assets(self) -> SupersetAssetsDef:
        return mk_assets(databases=[self.database], datasets=self.datasets)


class SupersetVisualizationBundle(SupersetAssetBundle):
    charts: list[SupersetChartDef] = pydantic.Field(default_factory=list)
    dashboards: list[SupersetDashboardDef] = pydantic.Field(default_factory=list)

    def to_assets(self) -> SupersetAssetsDef:
        return mk_assets(charts=self.charts, dashboards=self.dashboards)


class SupersetMitMDatasetBundle(SupersetAssetBundle):
    mitm_dataset: SupersetMitMDatasetDef
    datasource_bundle: SupersetDatasourceBundle
    visualization_bundle: SupersetVisualizationBundle = pydantic.Field(default_factory=SupersetVisualizationBundle)

    def to_assets(self) -> ExtendedSupersetAssetsDef:
        base_assets = mk_assets(databases=[self.datasource_bundle.database],
                                datasets=self.datasource_bundle.datasets,
                                charts=self.visualization_bundle.charts,
                                dashboards=self.visualization_bundle.dashboards)
        return mk_extended_assets(mitm_datasets=[self.mitm_dataset], base_assets=base_assets)
