from fastapi_versioned import FastAPIVersioned

from .api import versions
from .core import FakeDB

app = FastAPIVersioned(title="Example versioned app", versions=versions)
app.state.db = FakeDB()
