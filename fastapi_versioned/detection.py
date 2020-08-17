import pkgutil
import importlib
import re
from typing import List
from semantic_version import Version

from fastapi_versioned import VersionRouter

module_regex = re.compile("v[0-9]+_[0-9]+_[0-9]+")


def _module_to_version(module_name: str) -> Version:
    if not module_regex.match(module_name):
        raise ValueError(f"Unsupported module name '{module_name}'")

    return Version(module_name[1:].replace("_", "."))


def detect_versions(path: str, name: str) -> List[VersionRouter]:
    versions = []
    for module_info in pkgutil.iter_modules(path):
        module = importlib.import_module(f".{module_info.name}", name)
        try:
            version = getattr(module, "version")
            versions.append(version)
        except AttributeError as e:
            raise ImportError(f"Could not find 'version' attribute in module {module_info.name}")

    return versions
