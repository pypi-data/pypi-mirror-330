from ..definitions import SupersetMetadataDef, SupersetDatabaseDef, SupersetDashboardDef
from ..definitions.assets import MetadataType, SupersetAssetsDef, SupersetDatasetDef, SupersetChartDef, \
    ExtendedSupersetAssetsDef, SupersetMitMDatasetDef


def mk_metadata(metadata_type: MetadataType) -> SupersetMetadataDef:
    return SupersetMetadataDef(type=metadata_type)


def mk_assets(databases: list[SupersetDatabaseDef] = None,
              datasets: list[SupersetDatasetDef] = None,
              charts: list[SupersetChartDef] = None,
              dashboards: list[SupersetDashboardDef] = None,
              metadata_type: MetadataType | None = None) -> SupersetAssetsDef:
    return SupersetAssetsDef(databases=databases, datasets=datasets, charts=charts, dashboards=dashboards,
                             metadata=SupersetMetadataDef(type=metadata_type or MetadataType.Asset))


def mk_extended_assets(mitm_datasets: list[SupersetMitMDatasetDef],
                       base_assets: SupersetAssetsDef) -> ExtendedSupersetAssetsDef:
    return ExtendedSupersetAssetsDef(mitm_datasets=mitm_datasets, base_assets=base_assets)
