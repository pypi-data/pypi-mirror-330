import argparse
from pathlib import Path

from .code_autogen.graph_generator import generate_graph_code
from .code_autogen.schema_utils import read_schema, json_string_to_dict

def main():
    parser = argparse.ArgumentParser(description="Generate Python code for StepGraph from a schema definition.")
    parser.add_argument("schema_file", help="Path to the schema file (JSON or YAML)")
    args = parser.parse_args()

    schema_file_path = Path(args.schema_file)

    if not schema_file_path.exists():
        print(f"Error: Schema file not found at '{schema_file_path}'")
        exit(1)

    schema = json_string_to_dict(read_schema(schema_file_path))

    try:
        generated_code, _, _ = generate_graph_code(schema)
        print(generated_code)
    except Exception as e:
        print(f"Error during code generation: {e}")
        exit(1)

if __name__ == "__main__":
    main()
