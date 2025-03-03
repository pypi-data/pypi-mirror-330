import json
from typing import Any, Dict

# TODO: move base_classes/ to core/

graph_file_name = "execution_graph.py"
template_schema_file_name = "templates.json"
function_schema_file_name = "functions.json"
schema_file_name = "schema.json"

def json_string_to_dict(json_string: str) -> Dict[str, Any]:
    return json.loads(json_string)

def dict_to_json_string(dict: Dict[str, Any]) -> str:
     return json.dumps(dict)

def read_file(file_path: str) -> str:
    with open(file_path, 'r') as f:
        return f.read()

def write_file(file_path: str, content: str) -> str:
    with open(file_path, 'w') as f:
        return f.write(content)
