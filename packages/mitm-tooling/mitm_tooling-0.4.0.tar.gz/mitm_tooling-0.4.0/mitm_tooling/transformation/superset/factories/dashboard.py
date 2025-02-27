from typing import Any

from pydantic import UUID4

from mitm_tooling.transformation.superset.definitions import SupersetDashboardDef
from mitm_tooling.transformation.superset.factories.utils import mk_uuid


def mk_superset_dashboard(title: str,
                          position: dict[str, Any],
                          description: str | None = None,
                          uuid: UUID4 | None = None) -> SupersetDashboardDef:
    return SupersetDashboardDef(dashboard_title=title, position=position, description=description,
                                uuid=uuid or mk_uuid())
