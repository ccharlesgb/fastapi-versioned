from typing import Dict, List, Tuple, Any, Optional, Callable, Union

from fastapi import FastAPI, APIRouter
from openapi_schema_pydantic import OpenAPI
from semantic_version import Version

from .changelog import compare_openapi

__all__ = ["VersionRouter", "FastAPIVersioned"]


class VersionRouter:
    def __init__(self, version: Version, base: Optional['VersionRouter'] = None):
        self.router = APIRouter()
        if base:
            self.router.include_router(base.router)
        self.version = version

    def without(self, routes: List[Union[Callable, APIRouter]]):
        """
        Given a lits of view function endpoints or APIRoutes return the same version but without these included

        :param routes: A list of view functions (The endpoints of the route), or sub-routers
        :return: The same VersionRouter but with these removed
        """
        new_router = APIRouter()
        new_router.include_router(self.router)

        routes_expanded = []
        for excluded in routes:
            # TODO: Does this need to be recursive?
            if hasattr(excluded, "routes"):
                for route in excluded.routes:
                    routes_expanded.append(route.endpoint)
            else:
                routes_expanded.append(excluded)
        to_exclude = []
        for excluded_item in self.router.routes:
            if excluded_item.endpoint in routes_expanded:
                to_exclude.append(excluded_item)

        for excluded in to_exclude:
            new_router.routes.remove(excluded)

        new_version = VersionRouter(self.version)
        new_version.router = new_router
        return new_version


class FastAPIVersioned(FastAPI):
    def __init__(self, versions: List[VersionRouter], **kwargs):
        if "version" in kwargs:
            raise ValueError("Don't set the API version this will be handled for you")
        super().__init__(**kwargs)
        self._init_kwargs = kwargs
        self.version = "0.0.0"
        self._version_routers = versions
        self._sub_apps: List[Tuple[Version, FastAPI]] = []
        for version_router in sorted(self._version_routers, key=lambda val: val.version):
            self._add_version(version_router)

    def _add_version(self, version_router: VersionRouter):
        version_app = FastAPI(version=str(version_router.version), **self._init_kwargs)
        version_app.state.parent = self
        version_app.state.semver = version_router.version
        version_app.include_router(version_router.router)
        for index, (cur_version, _) in enumerate(self._sub_apps):
            if version_router.version < cur_version:
                insert_index = index
                break
        else:
            insert_index = len(self._sub_apps)
        self._sub_apps.insert(insert_index, (version_router.version, version_app))
        self.mount(f"/v{str(version_router.version)}", version_app)
        if version_router.version > Version(self.version):
            self.version = str(version_router.version)

    def get_version_changes(self) -> Dict[Tuple[Version, Version], Any]:
        if len(self._sub_apps) < 2:
            return {}
        changes: Dict[Tuple[Version, Version], Any] = {}
        # self._routers is always sorted by version
        for index in range(0, len(self._sub_apps) - 1):
            old_version, old_app = self._sub_apps[index]
            new_version, new_app = self._sub_apps[index + 1]
            new_openapi = OpenAPI.parse_obj(new_app.openapi())
            old_openapi = OpenAPI.parse_obj(old_app.openapi())
            changes[(new_version, old_version)] = compare_openapi(new_openapi, old_openapi)

        return changes
