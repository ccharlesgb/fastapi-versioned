"""
This is an example 'detectable' API to test that the folder structure is correctly interpreted
"""
from fastapi_versioned.detection import detect_versions

versions = detect_versions(__path__, __name__)
