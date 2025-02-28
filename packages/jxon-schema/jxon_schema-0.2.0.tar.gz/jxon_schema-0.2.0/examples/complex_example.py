#!/usr/bin/env python3
"""
Complex example of using the JXON library.
"""

import json
import os
import sys
import pprint

# Add parent directory to path for importing the library
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import jxon

# Complex nested JSON example
data = {
    "user_information": {
        "personal": {
            "name": "Jane Smith",
            "email": "jane@example.com",
            "age": 32
        },
        "address": {
            "street": "123 Main St",
            "city": "Anytown",
            "country": "USA",
            "postal_code": "12345"
        }
    },
    "app_settings": {
        "language_preference": {
            "description": "Languages the user wants in app",
            "current_value": ["English"]
        },
        "authentication": {
            "use_oauth2": {
                "description": "Whether OAuth2 is used for authentication",
                "current_value": False
            },
            "oauth_providers": ["Google", "GitHub"]
        },
        "ui_theme": {
            "description": "UI theme preference",
            "current_value": "light"
        }
    }
}

# Convert to schema
schema = jxon.convert_to_schema(data)

# Print the schema in a readable format
print("\n=== Complex Example Output ===\n")
print(json.dumps(schema, indent=2))

# Save to file
output_dir = os.path.join(os.path.dirname(__file__), "output")
os.makedirs(output_dir, exist_ok=True)
jxon.save_schema_to_file(schema, os.path.join(output_dir, "complex_example_output.json"))
