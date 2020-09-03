from semantic_version import Version

from fastapi_versioned import VersionRouter

from .. import v0_0_1
from . import users

# We are adding some new filter parameters to the updated API
modified_routes = [v0_0_1.users.views.get_all_users]

version = VersionRouter(Version("0.0.2"), base=v0_0_1.version.without(modified_routes))
version.router.include_router(users.router, prefix="/users")
