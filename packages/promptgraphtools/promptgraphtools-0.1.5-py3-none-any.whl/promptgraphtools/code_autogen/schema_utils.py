import json
from typing import Any, Dict

def json_string_to_dict(json_string: str) -> Dict[str, Any]:
    return json.loads(json_string)

def read_schema(schema_file_path: str) -> str:
    try:
        with open(schema_file_path, 'r') as f:
                return f.read()
    except Exception as e:
        print(f"Error reading schema file '{schema_file_path}': {e}")
        exit(1)
