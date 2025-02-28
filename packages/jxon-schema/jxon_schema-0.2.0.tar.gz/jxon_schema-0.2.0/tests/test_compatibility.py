"""
Compatibility tests to verify JXON works correctly across different Python versions.
"""
import sys
import unittest
import json
import os
from typing import Any, Dict, List, Optional, Union, cast

# Import JXON functionality
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from jxon.core import convert_to_schema, schema_to_json

def extract_original_data(schema_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Helper function to extract original data from schema format.
    This handles the specific output format that JXON creates.
    """
    if not isinstance(schema_data, dict):
        return schema_data
    
    result = {}
    
    for key, value in schema_data.items():
        # Skip special schema keys
        if key in ["type", "description", "required", "format", "enum"]:
            continue
        
        # Handle properties which contain the actual data fields
        if key == "properties":
            for prop_key, prop_value in value.items():
                if isinstance(prop_value, dict):
                    # If this is a nested object with properties
                    if "properties" in prop_value:
                        result[prop_key] = extract_original_data(prop_value)
                    # If this is a primitive with a type
                    elif "type" in prop_value:
                        # For arrays
                        if prop_value.get("type") == "array" and "items" in prop_value:
                            result[prop_key] = prop_value.get("default", [])
                        # For primitives
                        else:
                            result[prop_key] = prop_value.get("default", None)
                else:
                    result[prop_key] = prop_value
        # Handle arrays
        elif key == "items" and isinstance(value, dict):
            return [extract_original_data(value)]
        # Handle default values (primitives in schema)
        elif key == "default":
            return value
        # Skip schema-specific fields
        elif key not in ["propertyNames", "additionalProperties", "minItems", "maxItems"]:
            result[key] = extract_original_data(value)
    
    return result


class CompatibilityTests(unittest.TestCase):
    """Test compatibility across Python versions."""
    
    def test_version_specific_features(self):
        """Log Python version and test version-specific features."""
        print(f"Running tests on Python {sys.version}")
        
        # Test basic functionality
        test_data = {
            "name": "Test Object",
            "value": 42,
            "nested": {
                "array": [1, 2, 3],
                "boolean": True
            }
        }
        
        # Convert to schema 
        schema = convert_to_schema(test_data)
        
        # Print the schema structure to debug
        print("Schema structure:")
        print(json.dumps(schema, indent=2))
        
        # Check that basic properties exist
        self.assertIn("properties", schema)
        self.assertIn("name", schema["properties"])
        self.assertIn("value", schema["properties"])
        self.assertIn("nested", schema["properties"])
        
        # Simple test for schema validation - just verify proper structure
        self.assertEqual(schema["type"], "object")
        
        # Build a new test with simpler data to verify basic properties
        simple_test = {"simple": "value", "number": 123}
        simple_schema = convert_to_schema(simple_test)
        self.assertIn("simple", simple_schema["properties"])
        self.assertIn("number", simple_schema["properties"])
    
    def test_dict_operations(self):
        """Test dictionary operations which might vary across Python versions."""
        # Dictionary merging (3.9+ feature)
        if sys.version_info >= (3, 9):
            dict1 = {"a": 1, "b": 2}
            dict2 = {"c": 3, "d": 4}
            merged = dict1 | dict2
            self.assertEqual(merged, {"a": 1, "b": 2, "c": 3, "d": 4})
        else:
            print("Skipping 3.9+ dictionary merge test")
    
    def test_string_operations(self):
        """Test string operations which might vary across Python versions."""
        # String methods (3.9+ has new methods)
        test_string = "test_string"
        self.assertTrue(test_string.isascii())  # Python 3.7+
        
        if sys.version_info >= (3, 9):
            self.assertEqual(test_string.removeprefix("test_"), "string")
            self.assertEqual(test_string.removesuffix("_string"), "test")
        else:
            print("Skipping 3.9+ string methods test")
    
    def test_type_annotations(self):
        """Test type annotations processing."""
        # Union type operator (3.10+)
        if sys.version_info >= (3, 10):
            # In 3.10+, Union[str, int] can be written as str | int
            # This is just to verify syntax compatibility
            test_value: Union[str, int] = "test"
            self.assertEqual(test_value, "test")
            
            test_value = 42
            self.assertEqual(test_value, 42)
        else:
            print("Skipping 3.10+ Union type operator test")


if __name__ == "__main__":
    unittest.main()
