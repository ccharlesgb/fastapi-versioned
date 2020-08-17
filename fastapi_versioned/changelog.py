from enum import Enum
from typing import List, Any, Dict, Set, Tuple

from openapi_schema_pydantic import OpenAPI, PathItem, Operation
from pydantic import BaseModel

# List of method attributes for openapi_schema_pydantic
_http_methods = {"get", "head", "post", "put", "delete", "options", "trace", "patch"}


class ChangeCategory(Enum):
    ADDED = 1
    REMOVED = 2
    CHANGE = 3


class APIChange(BaseModel):
    breaking: bool
    category: ChangeCategory
    detail: str


class PathItemChange(PathItem):
    _changes: List[APIChange]


class OpenAPIChange(OpenAPI):
    _changes: List[APIChange]
    paths: Dict[str, PathItemChange]


def _get_added_removed_remain(new: Dict[Any, Any], old: Dict[Any, Any], include_none: bool = False) -> Tuple[
    Set, Set, Set]:
    if include_none:
        new_keys = set(new.keys())
        old_keys = set(old.keys())
    else:
        new_keys = set(k for k, v in new.items() if v is not None)
        old_keys = set(k for k, v in old.items() if v is not None)

    added_keys = new_keys - old_keys
    removed_keys = old_keys - new_keys
    remain_keys = new_keys.intersection(old_keys)
    return added_keys, removed_keys, remain_keys


def _extract_path_operations(path: PathItem) -> Dict[str, Operation]:
    operations = {}
    for method in _http_methods:
        operations[method] = getattr(path, method)
    return operations


def compare_openapi(new: OpenAPI, old: OpenAPI) -> List[APIChange]:
    api_changes: List[APIChange] = []

    added_paths, removed_paths, remain_paths = _get_added_removed_remain(new.paths, old.paths)

    # Removed paths are considered breaking changes
    for path in removed_paths:
        change = APIChange(breaking=True, category=ChangeCategory.REMOVED, detail=f"Path '{path}' has been removed")
        api_changes.append(change)

    # Added paths are not considered breaking
    for path in added_paths:
        change = APIChange(breaking=False, category=ChangeCategory.ADDED, detail=f"Path '{path}' has been added")
        api_changes.append(change)

    for path in remain_paths:
        new_path = new.paths[path]
        old_path = old.paths[path]
        api_changes.extend(_get_path_changes(new_path, old_path))

    return api_changes


def _get_path_changes(new_item: PathItem, old_item: PathItem) -> List[APIChange]:
    api_changes = []
    new_operations = _extract_path_operations(new_item)
    old_operations = _extract_path_operations(old_item)
    added_operations, removed_operations, remain_operations = _get_added_removed_remain(new_operations,
                                                                                        old_operations,
                                                                                        include_none=False)
    # Removing an operation will break clients that are using it
    for method in removed_operations:
        change = APIChange(breaking=True, category=ChangeCategory.REMOVED,
                           detail=f"Method '{method}' has been removed")
        api_changes.append(change)
    # An added operation is basically just a path addition so it should be non breaking
    for method in added_operations:
        change = APIChange(breaking=False, category=ChangeCategory.ADDED,
                           detail=f"Method '{method}' has been added")
        api_changes.append(change)

    # If the path operation is still there we need to check the parameters and body to see if anything has changed
    for method in remain_operations:
        new_operation = new_operations[method]
        old_operation = old_operations[method]
        api_changes.extend(_get_operation_changes(new_operation, old_operation))
    return api_changes


def _get_operation_changes(new_operation: Operation, old_operation: Operation) -> List[APIChange]:
    api_changes = []
    new_parameters = {elem.name: elem for elem in new_operation.parameters or []}
    old_parameters = {elem.name: elem for elem in old_operation.parameters or []}

    added_param, removed_param, remain_param = _get_added_removed_remain(new_parameters, old_parameters)

    for param_name in added_param:
        param = new_parameters[param_name]
        if param.required:
            change = APIChange(breaking=True, category=ChangeCategory.ADDED,
                               detail=f"Required parameter '{param_name}' has been added")
            api_changes.append(change)
        else:
            change = APIChange(breaking=False, category=ChangeCategory.ADDED,
                               detail=f"Optional parameter '{param_name}' has been added")
            api_changes.append(change)

    for param_name in removed_param:
        change = APIChange(breaking=True, category=ChangeCategory.REMOVED,
                           detail=f"Parameter '{param_name}' has been removed")
        api_changes.append(change)

    for param_name in remain_param:
        new_param = new_parameters[param_name]
        old_param = old_parameters[param_name]
        if new_param.param_in != old_param.param_in:
            change = APIChange(breaking=True, category=ChangeCategory.CHANGE,
                               detail=f"The parameter '{param_name}' has moved from '{old_param.param_in}' to "
                                      f"'{new_param.param_in}'")
            api_changes.append(change)
        # We could go further here and inspect the schema of the parameter for changes but lets stop for now

    return api_changes
