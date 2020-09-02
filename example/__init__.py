from fastapi_versioned import FastAPIVersioned
from .api import versions

app = FastAPIVersioned(title="Example versioned app", versions=versions)
