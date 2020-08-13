import pkgutil
import importlib
import re
from typing import Dict

from fastapi import APIRouter
from semantic_version import Version
from semantic_version import Version

module_regex = re.compile("v[0-9]+_[0-9]+_[0-9]+")


def _module_to_version(module_name: str) -> Version:
    if not module_regex.match(module_name):
        raise ValueError(f"Unsupported module name '{module_name}'")

    return Version(module_name[1:].replace("_", "."))


def detect_routers(path: str, name: str) -> Dict[Version, APIRouter]:
    routers = {}
    for module_info in pkgutil.iter_modules(path):
        module = importlib.import_module(f".{module_info.name}", name)
        try:
            router = getattr(module, "parent_router")
            routers[_module_to_version(module_info.name)] = router
        except AttributeError as e:
            raise ImportError(f"Could ont find 'parent_router' attribute in module {module_info.name}")

    return routers
