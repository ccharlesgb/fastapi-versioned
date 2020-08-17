from starlette.testclient import TestClient

from fastapi_versioned import FastAPIVersioned
from .detectable_api import versions as detected_versions


def test_version_detection():
    api = FastAPIVersioned(title="Test API", versions=detected_versions)

    client = TestClient(api)
    for i in [1, 2]:
        prefix = f"0.0.{i}"
        response = client.get(f"/v{prefix}/test{i}")
        assert response.status_code == 200
        assert response.json() == {"version": prefix}
