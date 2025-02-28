"""
JXON: JSON to Structured Output Schema Converter

This library converts normal JSON objects into structured output schemas
compatible with OpenAI's structured outputs feature.
"""

from .core import (
    convert_to_schema,
    load_json_file,
    save_schema_to_file,
    schema_to_json
)

__version__ = "0.1.0"
__all__ = [
    "convert_to_schema",
    "load_json_file",
    "save_schema_to_file",
    "schema_to_json",
]
