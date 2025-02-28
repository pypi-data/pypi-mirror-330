#!/usr/bin/env python3
"""
Array example of using the JXON library.
"""

import json
import os
import sys
import pprint

# Add parent directory to path for importing the library
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import jxon

# Array JSON example
data = {
    "todo_list": {
        "description": "User's todo list",
        "current_value": [
            "Buy groceries",
            "Call mom",
            "Finish report"
        ]
    },
    "tags": ["work", "personal", "urgent"],
    "completed_tasks": []
}

# Convert to schema
schema = jxon.convert_to_schema(data)

# Print the schema in a readable format
print("\n=== Array Example Output ===\n")
print(json.dumps(schema, indent=2))

# Save to file
output_dir = os.path.join(os.path.dirname(__file__), "output")
os.makedirs(output_dir, exist_ok=True)
jxon.save_schema_to_file(schema, os.path.join(output_dir, "array_example_output.json"))
