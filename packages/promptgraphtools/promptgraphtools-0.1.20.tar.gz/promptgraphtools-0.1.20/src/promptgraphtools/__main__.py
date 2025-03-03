import argparse
from pathlib import Path

from .code_autogen.graph_generator import generate_graph_code
from .code_autogen.io import read_file, json_string_to_dict, template_schema_file_name, function_schema_file_name, schema_file_name

def main():
    parser = argparse.ArgumentParser(description="Generate Python code for StepGraph from a schema definition.")
    args = parser.parse_args()

    schema_file_path = Path(schema_file_name)

    if not schema_file_path.exists():
        print(f"Error: Schema file not found at '{schema_file_path}'")
        exit(1)

    schema = json_string_to_dict(read_file(str(schema_file_path)))

    template_schema_file_path = Path(template_schema_file_name)
    template_schema = None

    if template_schema_file_path.exists():
        template_schema = json_string_to_dict(read_file(str(template_schema_file_path)))

    function_schema_file_path = Path(function_schema_file_name)
    function_schema = None

    if function_schema_file_path.exists():
        function_schema = json_string_to_dict(read_file(str(function_schema_file_path)))

    try:
        generate_graph_code(schema, function_schema, template_schema)
    except Exception as e:
        print(f"Error during code generation: {e}")
        exit(1)

if __name__ == "__main__":
    main()
