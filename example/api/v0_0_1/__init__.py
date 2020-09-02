from fastapi import APIRouter
from fastapi.requests import Request
from semantic_version import Version

from fastapi_versioned import VersionRouter

from . import users

version = VersionRouter(Version("0.0.1"))
version.router.include_router(users.router, prefix="/users")
