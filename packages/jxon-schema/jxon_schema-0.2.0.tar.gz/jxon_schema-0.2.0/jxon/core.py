"""
Core functionality for the JXON library.
"""

import json
import copy
from enum import Enum
from typing import Any, Dict, List, Optional, Union, Set, Tuple, TypeVar, cast

# Type definitions for better type hinting
JsonValue = Union[str, int, float, bool, None, Dict[str, Any], List[Any]]
JsonDict = Dict[str, JsonValue]
JsonList = List[JsonValue]
Schema = Dict[str, Any]

# Define an enum for schema types
class SchemaType(str, Enum):
    """Enum for schema types."""
    STRING = "string"
    INTEGER = "integer"
    NUMBER = "number"
    BOOLEAN = "boolean"
    NULL = "null"
    ARRAY = "array"
    OBJECT = "object"


def _pre_process_json(json_data: Any) -> Any:
    """
    Pre-process the JSON data to clean out schema elements and preserve important field data.
    
    Args:
        json_data: The JSON data to pre-process.
        
    Returns:
        The pre-processed JSON data with schema elements removed.
    """
    # Deep copy to avoid modifying the original
    result = None
    
    # Special case: if this is a dict with properties, handle specially
    if isinstance(json_data, dict):
        result = {}
        # Used to store custom descriptions for later use
        descriptions = {}
        
        # Check if this is an object with description and enum/values
        if "description" in json_data and ("enum" in json_data or "values" in json_data or "value" in json_data):
            # Store description
            desc = json_data["description"]
            
            if "enum" in json_data:
                # For enum fields, extract the enum values as a list
                enum_values = json_data["enum"]
                result = enum_values
                result = {"_descriptions": {"": desc}}
                return result
            elif "values" in json_data:
                # For fields with 'values', return the values with description
                values = json_data["values"]
                result = {"_descriptions": {"": desc}, "values": values}
                return result
            elif "value" in json_data:
                # For fields with single 'value', return the value with description
                value = json_data["value"]
                result = {"_descriptions": {"": desc}, "value": value}
                return result
        
        # Process each property
        for prop, value in json_data.items():
            # Skip schema-specific properties
            if prop in ["type", "properties", "items", "additionalProperties", "required"]:
                continue
                
            # Handle description specially
            if prop == "description":
                descriptions[""] = value
                continue
                
            # Keep custom_descriptions as is
            if prop == "_descriptions":
                result[prop] = value
                continue
                
            # Pre-process nested values
            processed_value = _pre_process_json(value)
            result[prop] = processed_value
            
        # If we collected descriptions, add them to result
        if descriptions:
            result["_descriptions"] = descriptions
            
    elif isinstance(json_data, list):
        # For lists, pre-process each item
        result = [_pre_process_json(item) for item in json_data]
    else:
        # For primitives, just return as is
        result = json_data
        
    return result


def convert_to_schema(
    json_data: Union[Dict[str, Any], List[Any], Any],
    include_description: bool = True,
    include_current_value: bool = True,
    add_required: bool = True,
    add_change_fields: bool = True,
    wrap_primitives: bool = False,
    custom_descriptions: Optional[Dict[str, str]] = None
) -> Schema:
    """
    Convert a JSON object to a schema object for editing.
    
    Args:
        json_data: JSON data to convert.
        include_description: Whether to include description fields.
        include_current_value: Whether to include current_value fields.
        add_required: Whether to add required fields.
        add_change_fields: Whether to add add/change fields for tracking changes.
        wrap_primitives: Whether to wrap primitive values (string, number, boolean) in objects with change fields.
        custom_descriptions: Optional dictionary of custom descriptions for fields.
        
    Returns:
        A schema for the JSON data.
    """
    # Pre-process JSON to clean schema elements and extract descriptions
    processed_data = _pre_process_json(json_data)
    
    # Create the schema
    schema = _create_schema(
        processed_data,
        include_description=include_description,
        include_current_value=include_current_value,
        add_required=add_required,
        add_change_fields=add_change_fields,
        wrap_primitives=wrap_primitives,
        descriptions_map=custom_descriptions
    )
                
    return schema


def _get_schema_type(value: Any) -> SchemaType:
    """
    Determine the schema type for a value.
    
    Args:
        value: The value to determine the type for.
        
    Returns:
        A SchemaType enum value.
    """
    if isinstance(value, str):
        return SchemaType.STRING
    elif isinstance(value, bool):
        return SchemaType.BOOLEAN
    elif isinstance(value, int):
        return SchemaType.INTEGER
    elif isinstance(value, float):
        return SchemaType.NUMBER
    elif value is None:
        return SchemaType.NULL
    elif isinstance(value, list):
        return SchemaType.ARRAY
    elif isinstance(value, dict):
        return SchemaType.OBJECT
    else:
        # Default fallback
        return SchemaType.STRING


def _create_primitive_schema(
    value: Any, 
    include_description: bool = True, 
    include_current_value: bool = True, 
    wrap_primitives: bool = False,
    add_change_fields: bool = False,
    field_name: Optional[str] = None,
    description: str = ""
) -> Schema:
    """
    Create a schema for a primitive value.
    
    Args:
        value: The value to create a schema for.
        include_description: Whether to include description fields.
        include_current_value: Whether to include current value fields.
        wrap_primitives: Whether primitives should be wrapped in objects.
        add_change_fields: Whether to add change fields.
        field_name: The name of the field.
        description: Description for the field.
        
    Returns:
        A schema dictionary.
    """
    # Get the schema type
    schema_type = _get_schema_type(value)
    
    # Create base schema
    schema = {
        "type": schema_type.value
    }
    
    # Add default values based on type
    if include_current_value:
        if schema_type == SchemaType.STRING:
            schema["current_value"] = ""
        elif schema_type == SchemaType.INTEGER:
            schema["current_value"] = 0
        elif schema_type == SchemaType.NUMBER:
            schema["current_value"] = 0.0
        elif schema_type == SchemaType.BOOLEAN:
            schema["current_value"] = False
        elif schema_type == SchemaType.NULL:
            schema["current_value"] = None
        else:
            # Default for any other type
            schema["current_value"] = ""
    
    # Add description if requested
    if include_description:
        schema["description"] = description
    
    return schema


def _create_array_schema(
    value: List[Any], 
    include_description: bool = True, 
    include_current_value: bool = False, 
    add_required: bool = True, 
    add_change_fields: bool = True, 
    field_name: Optional[str] = None, 
    description: str = "",
    wrap_primitives: bool = False,
    descriptions: Optional[Dict[str, str]] = None
) -> Schema:
    """Create a schema for an array value.
    
    Args:
        value: The array value.
        include_description: Whether to include a description.
        include_current_value: Whether to include the current value.
        add_required: Whether to add required fields.
        add_change_fields: Whether to add change fields.
        field_name: The field name this schema is for.
        description: The description for this field.
        wrap_primitives: Whether to wrap primitives in objects.
        descriptions: Dictionary of descriptions for fields.
        
    Returns:
        A schema dictionary.
    """
    # Check if this is a potential enum list (all primitives of same type)
    all_primitive = True
    all_same_type = True
    first_type = None
    
    for item in value:
        if isinstance(item, (list, dict)):
            all_primitive = False
            break
        
        item_type = _get_schema_type(item)
        if first_type is None:
            first_type = item_type
        elif first_type != item_type:
            all_same_type = False
            break
    
    # If this looks like an enum (all primitive values of same type), treat it as such
    if all_primitive and all_same_type and len(value) > 0 and first_type in [SchemaType.STRING, SchemaType.INTEGER, SchemaType.NUMBER]:
        enum_schema = {
            "type": "object",
            "additionalProperties": False,
            "properties": {
                "add": {
                    "type": "array",
                    "items": {
                        "type": first_type.value
                    }
                },
                "remove": {
                    "type": "array",
                    "items": {
                        "type": first_type.value
                    }
                },
                "replace": {
                    "type": "array",
                    "items": {
                        "type": first_type.value
                    }
                }
            },
            "required": ["add", "remove", "replace"]
        }
        
        if include_current_value:
            enum_schema["current_value"] = []
            
        if include_description:
            enum_schema["description"] = description
            
        return enum_schema
    
    # Regular array (not enum-like)
    schema = {
        "type": "object",
        "additionalProperties": False,
        "properties": {},
        "required": []
    }
    
    # If we need change fields, add them
    if add_change_fields:
        schema = _add_change_fields(
            value, 
            include_description=include_description,
            include_current_value=include_current_value,
            add_required=add_required,
            field_name=field_name
        )
    
    # Add description if requested
    if include_description:
        schema["description"] = description
        
    return schema


def _create_object_schema(
    obj: Dict[str, Any], 
    include_description: bool = True, 
    include_current_value: bool = False, 
    add_required: bool = True, 
    add_change_fields: bool = True, 
    wrap_primitives: bool = False,
    descriptions: Optional[Dict[str, str]] = None
) -> Schema:
    """Create a schema for an object.
    
    Args:
        obj: The object to create a schema for.
        include_description: Whether to include descriptions.
        include_current_value: Whether to include current values.
        add_required: Whether to add required fields.
        add_change_fields: Whether to add change fields.
        wrap_primitives: Whether to wrap primitives in objects.
        descriptions: Dictionary of descriptions for fields.
        
    Returns:
        A schema dictionary.
    """
    schema = {
        "type": "object",
        "additionalProperties": False,
        "properties": {},
    }
    
    # Add required field if requested and we have properties
    if add_required:
        schema["required"] = []
    
    # Extract any descriptions from a _descriptions field if present
    field_descriptions = {}
    if "_descriptions" in obj:
        field_descriptions = obj.get("_descriptions", {})
    
    # If a descriptions map was provided, use it to override field descriptions
    if descriptions:
        for field, desc in descriptions.items():
            field_descriptions[field] = desc
    
    # Add properties based on the object
    for key, value in obj.items():
        # Skip special fields
        if key == "_descriptions":
            continue
        
        # Get description for this field if available
        field_description = field_descriptions.get(key, f"{key}")
        
        # Create a schema for the property
        prop_schema = _create_schema(
            value, 
            include_description=include_description,
            include_current_value=include_current_value,
            add_required=add_required,
            add_change_fields=add_change_fields,
            field_name=key,
            wrap_primitives=wrap_primitives,
            descriptions_map=field_descriptions
        )
        
        schema["properties"][key] = prop_schema
        
        # Add to required list if requested
        if add_required and not key.startswith("_"):
            schema["required"].append(key)
    
    # Fix enum values based on the original object if applicable
    _fix_enum_in_properties(schema, obj)
    
    return schema


def _fix_enum_in_properties(schema: Schema, obj: Dict[str, Any]) -> None:
    """
    Fix enum values in schema properties.
    
    Args:
        schema: The schema to fix.
        obj: The original object that may contain enum values.
    """
    # Check if the object has enum values and the schema has properties
    if "enum" in obj and "properties" in schema:
        # If enum values exist at the top level, they apply to replace field
        if "replace" in schema.get("properties", {}):
            schema["properties"]["replace"]["enum"] = obj["enum"]
        
        # Process nested enum fields (specific to status and priority for now)
        # This should be made more generic in a future version
        for field_name in ["status", "priority"]:
            if field_name in schema.get("properties", {}) and "properties" in schema["properties"][field_name]:
                if "replace" in schema["properties"][field_name].get("properties", {}):
                    if "enum" in obj.get(field_name, {}):
                        schema["properties"][field_name]["properties"]["replace"]["enum"] = obj[field_name]["enum"]


def _add_change_fields(
    value: Any, 
    include_description: bool = True,
    include_current_value: bool = True,
    add_required: bool = True,
    field_name: Optional[str] = None
) -> Schema:
    """
    Add change fields to a primitive value schema.
    
    Args:
        value: The value to add change fields to.
        include_description: Whether to include description fields.
        include_current_value: Whether to include current_value fields.
        add_required: Whether to add required fields.
        field_name: The name of the field (for description purposes).
        
    Returns:
        A schema with change fields.
    """
    schema = {
        "type": "object",
        "additionalProperties": False,
        "properties": {},
        "required": []
    }
    
    # Add description and current_value if available
    if include_description and field_name:
        schema["description"] = f"{field_name}"
        
    if include_current_value:
        schema["current_value"] = value
        
    # For arrays, we handle them specially with add/remove fields
    if isinstance(value, list):
        # Get array item schema
        items_schema = _infer_array_item_schema(value)
        
        # Create change field properties for array operations
        for operation in ["add", "remove", "replace"]:
            operation_desc = {
                "add": f"Items to add to {field_name if field_name else 'Field'}",
                "remove": f"Items to remove from {field_name if field_name else 'Field'}",
                "replace": f"Replace all items with these in {field_name if field_name else 'Field'}"
            }
            
            schema["properties"][operation] = {
                "type": "array",
                "description": operation_desc[operation],
                "items": items_schema
            }
            
            if add_required:
                schema["required"].append(operation)
    else:
        # For non-arrays, we just have a replace field
        value_type = _get_schema_type(value)
        
        schema["properties"]["replace"] = {
            "type": value_type.value,
            "description": f"Value to replace {field_name if field_name else 'Field'} with"
        }
        
        if add_required:
            schema["required"].append("replace")
        
    return schema


def _infer_array_item_schema(arr: List[Any], wrap_primitives: bool = False) -> Schema:
    """
    Infer a schema for array items.
    
    Args:
        arr: The array to infer a schema for.
        wrap_primitives: Whether to wrap primitive values (string, number, boolean) in objects with change fields.
        
    Returns:
        A schema for array items.
    """
    # Empty array - default to string type
    if not arr:
        return {"type": "string"}
    
    # Check if all items are of the same primitive type
    first_item = arr[0]
    first_type = _get_schema_type(first_item)
    
    if first_type in [SchemaType.STRING, SchemaType.INTEGER, SchemaType.NUMBER, SchemaType.BOOLEAN, SchemaType.NULL]:
        all_same_type = all(_get_schema_type(item) == first_type for item in arr)
        
        if all_same_type:
            return {"type": first_type.value}
    
    # For mixed types or non-primitives, we need to determine the most common or appropriate type
    type_counts = {}
    for item in arr:
        item_type = _get_schema_type(item)
        type_counts[item_type] = type_counts.get(item_type, 0) + 1
    
    # Find the most common type
    if type_counts:
        most_common_type = max(type_counts.items(), key=lambda x: x[1])[0]
        return {"type": most_common_type.value}
    
    # Fallback to string
    return {"type": "string"}


def _create_primitive_change_schema(
    value: Any,
    include_description: bool = True,
    include_current_value: bool = True,
    add_required: bool = True,
    field_name: Optional[str] = None
) -> Schema:
    """
    Create a schema for a primitive value with change tracking.
    
    Args:
        value: The primitive value.
        include_description: Whether to include description fields.
        include_current_value: Whether to include current_value fields.
        add_required: Whether to add required fields.
        field_name: The name of the field (optional).
        
    Returns:
        A schema for the primitive with change tracking.
    """
    value_type = _get_schema_type(value)
    
    schema = {
        "type": "object",
        "additionalProperties": False,
        "properties": {
            "replace": {
                "type": value_type.value,
                "description": f"New value for {field_name if field_name else 'Field'}"
            }
        }
    }
    
    if add_required:
        schema["required"] = ["replace"]
        
    if include_description and field_name:
        schema["description"] = f"{field_name}"
        
    if include_current_value:
        schema["current_value"] = value
        
    return schema


def _create_schema(
    value: Any, 
    include_description: bool = True, 
    include_current_value: bool = False,
    add_required: bool = True,
    add_change_fields: bool = True,
    field_name: Optional[str] = None,
    wrap_primitives: bool = False,
    descriptions_map: Optional[Dict[str, str]] = None
) -> Schema:
    """Create a schema for a value.
    
    Args:
        value: The value to create a schema for.
        include_description: Whether to include descriptions.
        include_current_value: Whether to include current values.
        add_required: Whether to add required fields.
        add_change_fields: Whether to add change fields.
        field_name: The name of the field (for description purposes).
        wrap_primitives: Whether to wrap primitives in objects.
        descriptions_map: Dictionary of descriptions for fields.
        
    Returns:
        A schema dictionary.
    """
    description = ""
    
    # Get description from descriptions_map if available
    if descriptions_map and field_name and field_name in descriptions_map:
        description = descriptions_map[field_name]
    
    # Handle dictionaries (objects)
    if isinstance(value, dict):
        return _create_object_schema(
            value,
            include_description=include_description,
            include_current_value=include_current_value,
            add_required=add_required,
            add_change_fields=add_change_fields,
            wrap_primitives=wrap_primitives,
            descriptions=descriptions_map
        )
    
    # Handle lists (arrays)
    elif isinstance(value, list):
        return _create_array_schema(
            value,
            include_description=include_description,
            include_current_value=include_current_value,
            add_required=add_required,
            add_change_fields=add_change_fields,
            field_name=field_name,
            description=description,
            wrap_primitives=wrap_primitives,
            descriptions=descriptions_map
        )
    
    # Handle primitives
    else:
        if wrap_primitives and add_change_fields:
            # Wrap the primitive in an object
            return _create_primitive_change_schema(
                value,
                include_description=include_description,
                include_current_value=include_current_value,
                add_required=add_required,
                field_name=field_name
            )
        else:
            # Just create a basic primitive schema
            return _create_primitive_schema(
                value,
                include_description=include_description,
                include_current_value=include_current_value,
                wrap_primitives=wrap_primitives,
                field_name=field_name,
                description=description
            )


def load_json_file(file_path: str) -> JsonDict:
    """
    Load JSON data from a file.
    
    Args:
        file_path: The path to the JSON file.
        
    Returns:
        The loaded JSON data.
    """
    with open(file_path, 'r') as f:
        return json.load(f)


def schema_to_json(schema: Schema, indent: int = 4) -> str:
    """
    Convert a schema to a JSON string.
    
    Args:
        schema: The schema to convert.
        indent: The indentation level for the JSON output.
        
    Returns:
        A JSON string representation of the schema.
    """
    return json.dumps(schema, indent=indent)


def save_schema_to_file(schema: Schema, file_path: str, indent: int = 4) -> None:
    """
    Save a schema to a JSON file.
    
    Args:
        schema: The schema to save.
        file_path: The path to save the schema to.
        indent: The indentation level for the JSON output.
    """
    with open(file_path, 'w') as f:
        json.dump(schema, f, indent=indent)
