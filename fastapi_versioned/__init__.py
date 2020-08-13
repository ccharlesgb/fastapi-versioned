from fastapi import FastAPI, APIRouter
from .detection import detect_routers
from semantic_version import Version


class FastAPIParent(FastAPI):

    def __init__(self, **kwargs):
        if "version" in kwargs:
            raise ValueError("Don't set the API version this will be handled for you")
        super().__init__(**kwargs)
        self._init_kwargs = kwargs
        self.version = "0.0.0"

    def add_version(self, prefix: Version, router: APIRouter):
        version_app = FastAPIVersion(self, prefix, **self._init_kwargs)
        version_app.include_router(router)
        self.mount(f"/v{str(prefix)}", version_app)
        if prefix > Version(self.version):
            self.version = str(prefix)


class FastAPIVersion(FastAPI):
    def __init__(self, parent: FastAPIParent, version: Version, **kwargs):
        super().__init__(verison=str(version), **kwargs)
        self.parent = parent
        self.version = version
