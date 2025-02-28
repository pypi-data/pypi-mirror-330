#!/usr/bin/env python3
"""
Simple example of using the JXON library.
"""

import json
import os
import sys
import pprint

# Add parent directory to path for importing the library
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import jxon

# Simple JSON example
data = {
    "username": "johndoe",
    "email": "john@example.com",
    "preferences": {
        "description": "User preferences",
        "current_value": {
            "theme": "dark",
            "notifications": True,
            "languages": ["English", "Spanish"]
        }
    }
}

# Convert to schema
schema = jxon.convert_to_schema(data)

# Print the schema in a readable format
print("\n=== Simple Example Output ===\n")
print(json.dumps(schema, indent=2))

# Save to file
output_dir = os.path.join(os.path.dirname(__file__), "output")
os.makedirs(output_dir, exist_ok=True)
jxon.save_schema_to_file(schema, os.path.join(output_dir, "simple_example_output.json"))
