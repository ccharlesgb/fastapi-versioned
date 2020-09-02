# fastapi-versioned

Adds versioning to a fast API application based on the idea that each API version has a parent `APIRouter` and it can
inherit various routes/sub-routers from the previous version.
