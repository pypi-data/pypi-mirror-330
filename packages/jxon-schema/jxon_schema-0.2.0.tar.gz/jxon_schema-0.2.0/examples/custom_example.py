#!/usr/bin/env python3
"""
Example showing customization options of the JXON library.
"""

import json
import os
import sys
import pprint

# Add parent directory to path for importing the library
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import jxon

# Sample JSON data
data = {
    "product": {
        "description": "Product information",
        "current_value": {
            "name": "Smart Watch",
            "price": 199.99,
            "in_stock": True,
            "colors": ["Black", "Silver", "Gold"]
        }
    },
    "categories": ["Electronics", "Wearables", "Fitness"]
}

# Example 1: Default behavior (with add/remove/replace fields)
schema_default = jxon.convert_to_schema(data)

# Example 2: Without change fields (just convert structure)
schema_no_change = jxon.convert_to_schema(
    data, 
    add_change_fields=False
)

# Example 3: Without description and current_value
schema_minimal = jxon.convert_to_schema(
    data,
    include_description=False,
    include_current_value=False
)

# Print the schemas in a readable format
print("\n=== Default Schema (with change fields) ===\n")
print(json.dumps(schema_default, indent=2))

print("\n=== Schema without Change Fields ===\n")
print(json.dumps(schema_no_change, indent=2))

print("\n=== Minimal Schema (no descriptions or current values) ===\n")
print(json.dumps(schema_minimal, indent=2))

# Save to files
output_dir = os.path.join(os.path.dirname(__file__), "output")
os.makedirs(output_dir, exist_ok=True)

jxon.save_schema_to_file(schema_default, os.path.join(output_dir, "custom_example_default.json"))
jxon.save_schema_to_file(schema_no_change, os.path.join(output_dir, "custom_example_no_change.json"))
jxon.save_schema_to_file(schema_minimal, os.path.join(output_dir, "custom_example_minimal.json"))
