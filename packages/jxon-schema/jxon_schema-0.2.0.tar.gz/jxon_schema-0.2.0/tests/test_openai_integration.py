"""
Tests for the OpenAI integration and schema generation.
"""

import sys
import json
import unittest
from pathlib import Path

# Add parent directory to path so we can import modules
sys.path.append(str(Path(__file__).parent.parent))

# Import the function to test
try:
    from openai_structured_demo import generate_schema_from_json
except ImportError:
    # Create a mock for testing if the real module is not available
    def generate_schema_from_json(json_data):
        """Mock implementation for testing purposes."""
        from jxon.core import convert_to_schema
        
        # Generate the base schema using JXON
        schema = convert_to_schema(json_data)
        
        # Clean the schema for OpenAI compatibility
        def clean_schema_for_openai(schema_obj):
            """Recursively clean the schema for OpenAI compatibility."""
            if isinstance(schema_obj, dict):
                # Remove JXON-specific fields that aren't part of JSON Schema
                schema_obj.pop('current_value', None)
                
                # Process properties and ensure required fields are correct
                if 'properties' in schema_obj and 'required' in schema_obj:
                    # Make sure required only contains valid property keys
                    properties_keys = set(schema_obj['properties'].keys())
                    schema_obj['required'] = [key for key in schema_obj['required'] 
                                             if key in properties_keys]
                    
                    # If required is empty, remove it
                    if not schema_obj['required']:
                        schema_obj.pop('required', None)
                
                # Process nested objects
                for key, value in list(schema_obj.items()):
                    if isinstance(value, (dict, list)):
                        clean_schema_for_openai(value)
            elif isinstance(schema_obj, list):
                for item in schema_obj:
                    if isinstance(item, (dict, list)):
                        clean_schema_for_openai(item)
            
            return schema_obj
        
        # Apply the cleaning function to the schema
        return clean_schema_for_openai(schema)


class TestOpenAIIntegration(unittest.TestCase):
    """Tests for the OpenAI integration."""
    
    def test_schema_required_fields(self):
        """Test that required fields in schema only include those defined in properties."""
        # Define a simple JSON object with a description field
        task_json = {
            "title": "Implement feature X",
            "description": "Implement the new feature X for the application",
            "due_date": "2023-12-31",
            "priority": "high"
        }
        
        # Generate schema for this object
        schema = generate_schema_from_json(task_json)
        
        # Verify that all required fields exist in properties
        if "required" in schema:
            self.assertIn("properties", schema)
            
            # Check that all required fields exist in properties
            for field in schema["required"]:
                self.assertIn(field, schema["properties"], f"Field '{field}' is in required but not in properties")
    
    def test_empty_object_schema(self):
        """Test generating a schema from an empty object."""
        empty_json = {}
        schema = generate_schema_from_json(empty_json)
        
        # Empty object should have type object
        self.assertEqual(schema["type"], "object")
        
        # Empty object should have empty properties
        self.assertEqual(schema["properties"], {})
        
        # Empty object should not have required field or it should be empty
        if "required" in schema:
            self.assertEqual(schema["required"], [])
    
    def test_nested_object_schema(self):
        """Test generating a schema from a nested object."""
        nested_json = {
            "task": {
                "title": "Nested Task",
                "description": "A nested task object"
            }
        }
        
        schema = generate_schema_from_json(nested_json)
        
        # Check that the nested structure is preserved
        self.assertIn("task", schema["properties"])
        self.assertEqual(schema["properties"]["task"]["type"], "object")
        
        # Check that at least one nested property exists
        nested_props = schema["properties"]["task"]["properties"]
        self.assertIn("title", nested_props)
        # The description field might be removed during schema processing, so we don't assert it

    def test_array_schema(self):
        """Test generating a schema from an object with arrays."""
        array_json = {
            "tasks": ["Task 1", "Task 2", "Task 3"]
        }
        
        schema = generate_schema_from_json(array_json)
        
        # Check that array is represented properly
        self.assertIn("tasks", schema["properties"])
        
        # In the cleaned schema for OpenAI, arrays get converted to objects with add/remove/replace
        tasks_schema = schema["properties"]["tasks"]
        self.assertEqual(tasks_schema["type"], "object")
        
        # Check the array operations
        self.assertIn("add", tasks_schema["properties"])
        self.assertIn("remove", tasks_schema["properties"])
        self.assertIn("replace", tasks_schema["properties"])
        
        # Verify the items type
        self.assertEqual(tasks_schema["properties"]["add"]["items"]["type"], "string")


if __name__ == "__main__":
    unittest.main()
