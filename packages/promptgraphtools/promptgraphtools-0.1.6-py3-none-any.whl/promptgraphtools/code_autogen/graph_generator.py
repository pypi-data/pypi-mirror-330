from typing import Any, Dict, Set, Tuple, Optional
from .io import write_file, dict_to_json_string, function_schema_file_name, template_schema_file_name, graph_file_name

def generate_graph_code(schema: Dict[str, Any], function_schema: Optional[Dict[str, str]] = None, template_schema: Optional[Dict[str, str]] = None) -> Tuple[str, Dict[str, str], Dict[str, str]]:
    function_definitions_code, step_definitions_code, main_graph_code, import_lines, template_definitions_code, generated_function_names, generated_template_names = _generate_graph_code_recursive(schema)
    consolidated_imports_code = _consolidate_imports_to_string(import_lines)

    final_code = f"""{consolidated_imports_code}\n{function_definitions_code}\n{template_definitions_code}\n{step_definitions_code}\n{main_graph_code}"""

    function_name_dict = {name: "" for name in generated_function_names}
    template_name_dict = {name: "" for name in generated_template_names}

    if not function_schema:
        functions = dict_to_json_string(function_name_dict)
        write_file(function_schema_file_name, functions)
    
    if not template_schema:
        templates = dict_to_json_string(template_name_dict)
        write_file(template_schema_file_name, templates)
    
    for key, value in function_name_dict:
        set_function_code(final_code, key, value)

    for key, value in template_name_dict:
        set_template_code(final_code, key, value)
    
    write_file(graph_file_name, final_code)

    return final_code, function_name_dict, template_name_dict

def _generate_graph_code_recursive(schema: Dict[str, Any], generated_function_names: Set[str] = None, collected_import_lines: Set[str] = None, generated_template_names: Set[str] = None) -> Tuple[str, str, str, Set[str], str, Set[str], Set[str]]:
    """
    Recursively generates code components for a StepGraph and its subgraphs, referencing LLM client definitions.
    Returns code components along with sets of generated function and template names.

    Args:
        schema (Dict[str, Any]): Schema for the current graph level.
        generated_function_names (Set[str], optional): Set to track function names (for de-duplication).
        collected_import_lines (Set[str], optional): Set to accumulate import lines.
        generated_template_names (Set[str], optional): Set to track template names (for de-duplication).

    Returns:
        Tuple[str, str, str, Set[str], str, Set[str], Set[str]]: Function definitions, step definitions,
                                                 main graph code, collected import lines, template definitions,
                                                 generated function names, generated template names for this level.
    """
    if generated_function_names is None:
        generated_function_names = set()
    if collected_import_lines is None:
        collected_import_lines = set()
    if generated_template_names is None:
        generated_template_names = set()

    graph_name = schema.get("graph_name")
    required_inputs = schema.get("required_inputs")
    required_outputs = schema.get("required_outputs")
    config = schema.get("configuration")
    steps_schema = config.get("steps")
    dependencies_schema = config.get("dependencies")
    llm_clients_schema = schema.get("llm_clients", {})

    step_definitions_code = ""
    step_instantiations_code = ""
    dependencies_code = "    dependencies = {\n"
    function_definitions_code = ""
    template_definitions_code = ""

    collected_import_lines.update([
        "from typing import Any, Dict, List",
        "from promptgraphtools.core.step_graph import StepGraph",
        "from promptgraphtools.core.step import Step",
        "from promptgraphtools.core.fan_out_step import FanOutStep",
        "from promptgraphtools.core.conditional_router_step import ConditionalRouterStep",
        "from promptgraphtools.base_classes.step_like import StepLike"
    ])


    immediate_step_definitions = []
    deferred_step_definitions: Dict[str, Dict[str, Any]] = {}

    for step_def in steps_schema:
        step_name = step_def.get("step_name")
        step_type = step_def.get("step_type")
        required_inputs_step = step_def.get("required_inputs")
        required_outputs_step = step_def.get("required_outputs")
        step_config = step_def.get("configuration")

        if step_type == "Step":
            function_ref = step_config.get("function")
            llm_client = step_config.get("llm_client")
            end_tag = step_config.get("end_tag")
            end_instructions = step_config.get("end_instructions")

            if function_ref:
                function_name = function_ref.split(".")[-1]
                if function_name not in generated_function_names:
                    function_definitions_code += f"def {function_name}(inputs: Dict[str, Any]) -> Dict[str, Any]:\n"
                    function_definitions_code += f'    pass\n    # END_OF_FUNCTION\n\n'
                    generated_function_names.add(function_name)
                step_instantiation = f"""\
    {step_name} = Step(
        step_name='{step_name}',
        required_inputs={required_inputs_step},
        required_outputs={required_outputs_step},
        function={function_name},
    )
"""
                immediate_step_definitions.append(step_instantiation)
            elif llm_client:
                template_var_name = f"{step_name.replace(' ', '_').replace('-', '_').replace('.', '_')}_template"
                if template_var_name not in generated_template_names:
                    template_definitions_code += f"{template_var_name} = \"\"\"\n# Define your template string for step: {step_name} here \n\"\"\"\n\n"
                    generated_template_names.add(template_var_name)

                step_instantiation = f"""\
    {step_name} = Step(
        step_name='{step_name}',
        required_inputs={required_inputs_step},
        required_outputs={required_outputs_step},
        template={template_var_name},
        llm_client={llm_client},
"""
                if end_tag:
                    step_instantiation += f"        end_tag='{end_tag}',\n"
                if end_instructions:
                    step_instantiation += f"        end_instructions='{end_instructions}',\n"
                step_instantiation += f"    )\n"
                immediate_step_definitions.append(step_instantiation)
            else:
                raise ValueError(f"Step '{step_name}' configuration is invalid.")

        elif step_type == "FanOutStep":
            input_key = step_config.get("input_key")
            output_key = step_config.get("output_key", "results")
            fan_out_function_ref = step_config.get("function")
            llm_client = step_config.get("llm_client")
            step_graph_ref = step_config.get("step_graph")
            concurrency = step_config.get("concurrency", 5)
            batch_mode = step_config.get("batch_mode", True)

            if fan_out_function_ref:
                function_name = fan_out_function_ref.split(".")[-1]
                if function_name not in generated_function_names:
                    function_definitions_code += f"def {function_name}(item: Any, inputs: Dict[str, Any]) -> Dict[str, Any]:\n"
                    function_definitions_code += f'    """\n    Placeholder function for fan-out step: {step_name}\n    Implement your function logic here.\n    """\n    pass\n\n'
                    generated_function_names.add(function_name)
                step_instantiation = f"""\
    {step_name} = FanOutStep(
        step_name='{step_name}',
        required_inputs={required_inputs_step},
        required_outputs={required_outputs_step},
        input_key='{input_key}',
        output_key='{output_key}',
        function={function_name},
        concurrency={concurrency},
        batch_mode={batch_mode},
    )
"""
                immediate_step_definitions.append(step_instantiation) # Define FanOutSteps with function or llm_client immediately as well
            elif llm_client:
                template_var_name = f"{step_name.replace(' ', '_').replace('-', '_').replace('.', '_')}_template"
                if template_var_name not in generated_template_names:
                    template_definitions_code += f"{template_var_name} = \"\"\" # Define your template string for fan-out step: {step_name} here \n\"\"\"\n\n"
                    generated_template_names.add(template_var_name)

                step_instantiation = f"""\
    {step_name} = FanOutStep(
        step_name='{step_name}',
        required_inputs={required_inputs_step},
        required_outputs={required_outputs_step},
        input_key='{input_key}',
        output_key='{output_key}',
        template={template_var_name},
        llm_client={llm_client},
        concurrency={concurrency},
        batch_mode={batch_mode},
    )
"""
                immediate_step_definitions.append(step_instantiation) # Define FanOutSteps with function or llm_client immediately as well
            elif step_graph_ref: # step_graph_ref is now just a name string
                # NO RECURSIVE CALL HERE for FanOutStep with step_graph_ref!
                step_graph_function_name = f"build_{step_graph_ref.replace(' ', '_').replace('-', '_').replace('.', '_')}_graph"
                step_instantiation = f"""\
    {step_name} = FanOutStep(
        step_name='{step_name}',
        required_inputs={required_inputs_step},
        required_outputs={required_outputs_step},
        input_key='{input_key}',
        output_key='{output_key}',
        step_graph={step_graph_function_name}(),
        concurrency={concurrency},
        batch_mode={batch_mode},
    )
"""
                deferred_step_definitions[step_name] = {'code_blob': step_instantiation, 'depends_on': [step_graph_ref]} # Added to dict

        elif step_type == "ConditionalRouterStep":
            steps_config = step_config.get("steps")
            default_step_ref = step_config.get("default")

            steps_route_map_code = "{"
            route_steps = []
            depends_on_steps = [] # Collect dependencies for ConditionalRouterStep
            for route_key, route_step_name in steps_config.items():
                step_ref_name = route_step_name.get('step_name')
                if step_ref_name:
                    route_steps.append(f"'{route_key}': {step_ref_name}")
                    depends_on_steps.append(step_ref_name) # Add dependency
                else:
                    raise ValueError(f"ConditionalRouterStep '{step_name}' route is missing 'step_name'.")

            steps_route_map_code += ", ".join(route_steps) + "}"

            default_step_code = f"{default_step_ref}" if default_step_ref else "None"

            step_instantiation = f"""\
    {step_name} = ConditionalRouterStep(
        name='{step_name}',
        required_inputs={required_inputs_step},
        required_outputs={required_outputs_step},
        steps={steps_route_map_code},
        default={default_step_code},
    )
"""
            deferred_step_definitions[step_name] = {'code_blob': step_instantiation, 'depends_on': depends_on_steps} # Added to dict with dependencies


        elif step_type == "StepGraph":
            subgraph_step_name = step_name
            subgraph_required_inputs = required_inputs_step
            subgraph_required_outputs = required_outputs_step

            # Recursive call to generate subgraph code, passing function name and import sets
            sub_function_defs, sub_step_defs, sub_main_graph_code, sub_imports, sub_template_defs, sub_generated_function_names, sub_generated_template_names = _generate_graph_code_recursive( # Note order change in return values
                schema={ "configuration": step_config, "graph_name": subgraph_step_name, "required_inputs": subgraph_required_inputs, "required_outputs": subgraph_required_outputs, "llm_clients": llm_clients_schema}, # Pass llm_clients_schema down
                generated_function_names=generated_function_names,
                collected_import_lines=collected_import_lines,
                generated_template_names=generated_template_names,
            )
            function_definitions_code += sub_function_defs
            step_definitions_code += sub_step_defs
            step_definitions_code += f"\n{sub_main_graph_code}\n"
            template_definitions_code += sub_template_defs
            collected_import_lines.update(sub_imports)
            generated_function_names.update(sub_generated_function_names)
            generated_template_names.update(sub_generated_template_names)


            subgraph_function_name = f"build_{subgraph_step_name.replace(' ', '_').replace('-', '_').replace('.', '_')}_graph"
            step_instantiation = f"    {step_name} = {subgraph_function_name}()\n"
            deferred_step_definitions[step_name] = {'code_blob': step_instantiation, 'depends_on': []} # Added to dict

        else:
            raise ValueError(f"Unknown step type: {step_type}")

    # First add immediate step definitions, then deferred ones
    step_instantiations_code += "".join(immediate_step_definitions)

    # Order deferred steps by dependency count
    ordered_deferred_steps = sorted(deferred_step_definitions.items(), key=lambda item: len(item[1]['depends_on']))
    for step_name, step_data in ordered_deferred_steps:
        step_instantiations_code += step_data['code_blob']


    for step_name, deps in dependencies_schema.items():
        deps_str = "[" + ", ".join([f"'{dep}'" for dep in deps]) + "]" if deps else "[]"
        dependencies_code += f"        '{step_name}': {deps_str},\n"
    dependencies_code += "    }\n"

    llm_client_definitions_for_this_graph = ""
    if llm_clients_schema:
        collected_import_lines.add("from pipelines.llm_clients.gemini import Gemini")
        for client_name, client_config in llm_clients_schema.items():
            llm_client_definitions_for_this_graph += f"    {client_name} = Gemini(\n"
            llm_client_definitions_for_this_graph += f"        model=Gemini.Models.{client_config['model'].upper().replace('-', '_')},\n"
            llm_client_definitions_for_this_graph += f"        max_output_tokens={client_config['max_output_tokens']},\n"
            llm_client_definitions_for_this_graph += f"        temperature={client_config['temperature']},\n"
            llm_client_definitions_for_this_graph += f"        top_p={client_config['top_p']},\n"
            llm_client_definitions_for_this_graph += f"        use_tools={client_config['use_tools']},\n"
            llm_client_definitions_for_this_graph += f"    )\n\n"


    main_graph_code = f"""
def build_{graph_name.replace(' ', '_').replace('-', '_').replace('.', '_')}_graph() -> StepLike:
    \"\"\"
    Builds the {graph_name} StepGraph.
    \"\"\"
{llm_client_definitions_for_this_graph}{step_instantiations_code}
{dependencies_code}

    return StepGraph(
        graph_name='{graph_name}',
        steps=[{', '.join([step_name for step_name in dependencies_schema.keys()])}],
        dependencies=dependencies,
        required_inputs={required_inputs},
        required_outputs={required_outputs},
    )
"""
    return function_definitions_code, step_definitions_code, main_graph_code, collected_import_lines, template_definitions_code, generated_function_names, generated_template_names

def _consolidate_imports_to_string(import_lines: Set[str]) -> str:
    """Converts a set of import lines to a sorted string block."""
    return "\n".join(sorted(list(import_lines))) + "\n\n"

def get_function_code(code_blob: str, function_name: str) -> str:
    """
    Extracts the code block of a function from a code string.

    Args:
        code_blob (str): The string containing the Python code.
        function_name (str): The name of the function to extract.

    Returns:
        str: The code block of the function, including the definition line and the end of function tag,
             or None if the function is not found.
    """
    start_marker = f"def {function_name}"
    end_marker = "# END_OF_FUNCTION"

    start_index = code_blob.find(start_marker)
    if start_index == -1:
        return None

    end_index = code_blob.find(end_marker, start_index)
    if end_index == -1:
        return None

    return code_blob[start_index:end_index + len(end_marker) + 1] # +1 to include the newline after the tag

def get_template_code(code_blob: str, template_var_name: str) -> str:
    """
    Extracts the content of a template string from a code string.

    Args:
        code_blob (str): The string containing the Python code.
        template_var_name (str): The variable name of the template to extract.

    Returns:
        str: The template string content, including the variable assignment and triple quotes,
             or None if the template is not found.
    """
    start_marker = f"{template_var_name} = \"\"\""
    end_marker = "\"\"\""

    start_index = code_blob.find(start_marker)
    if start_index == -1:
        return None

    start_content_index = start_index + len(start_marker)
    end_index = code_blob.find(end_marker, start_content_index)
    if end_index == -1:
        return None

    return code_blob[start_index:end_index + len(end_marker)]

def set_function_code(code_blob: str, function_name: str, new_function_code: str) -> str:
    """
    Replaces the code block of a function in a code string with new code.

    Args:
        code_blob (str): The string containing the Python code.
        function_name (str): The name of the function to replace.
        new_function_code (str): The new code block for the function.

    Returns:
        str: The modified code string with the function code replaced,
             or the original code_blob if the function is not found.
    """
    old_function_code = get_function_code(code_blob, function_name)
    if old_function_code is None:
        raise Exception(f"error: no function named {function_name} in code blob")

    return code_blob.replace(old_function_code, new_function_code)

def set_template_code(code_blob: str, template_var_name: str, new_template_code: str) -> str:
    """
    Replaces the content of a template string in a code string with new content.

    Args:
        code_blob (str): The string containing the Python code.
        template_var_name (str): The variable name of the template to replace.
        new_template_code (str): The new template string content (without variable assignment and triple quotes).

    Returns:
        str: The modified code string with the template content replaced,
             or the original code_blob if the template is not found.
    """
    old_template_code = get_template_code(code_blob, template_var_name)
    if old_template_code is None:
        raise Exception(f"error: no template named {template_var_name} in code blob")

    new_template_definition = f"{template_var_name} = \"\"\"\n{new_template_code}\n\"\"\""
    return code_blob.replace(old_template_code, new_template_definition)
