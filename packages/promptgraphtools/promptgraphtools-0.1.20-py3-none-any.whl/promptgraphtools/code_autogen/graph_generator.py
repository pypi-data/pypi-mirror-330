from typing import Any, Dict, Set, Tuple, Optional
from .io import write_file, dict_to_json_string, function_schema_file_name, template_schema_file_name, graph_file_name
import os

def generate_graph_code(schema: Dict[str, Any], function_schema: Optional[Dict[str, str]] = None, template_schema: Optional[Dict[str, str]] = None) -> Tuple[str, Dict[str, str], Dict[str, str]]:
    function_definitions_code, step_definitions_code, main_graph_code, import_lines, template_definitions_code, generated_function_names, generated_template_names, function_name_map, template_name_map = _generate_graph_code_recursive(schema)
    consolidated_imports_code = _consolidate_imports_to_string(import_lines)

    functions_schema_content = {}
    templates_schema_content = {}

    # Handle function schemas and files
    if function_schema:
        function_name_map = function_schema
    else:
        for function_file_name in generated_function_names:
            functions_schema_content[function_file_name] = f"functions/{function_file_name}.py"
            function_name_map[function_file_name] = f"functions/{function_file_name}.py"
            os.makedirs(os.path.dirname(f"functions/{function_file_name}.py"), exist_ok=True)
            write_file(f"functions/{function_file_name}.py", function_definitions_code[function_file_name])

        functions = dict_to_json_string(functions_schema_content)
        write_file(function_schema_file_name, functions)

    # Handle template schemas and files
    if template_schema:
        template_name_map = template_schema
    else:
        for template_file_name in generated_template_names:
            templates_schema_content[template_file_name] = f"templates/{template_file_name}.py"
            template_name_map[template_file_name] = f"templates/{template_file_name}.py"
            os.makedirs(os.path.dirname(f"templates/{template_file_name}.py"), exist_ok=True)
            write_file(f"templates/{template_file_name}.py", template_definitions_code[template_file_name])

        templates = dict_to_json_string(templates_schema_content)
        write_file(template_schema_file_name, templates)

    # Generate final code with imports and graph definition
    final_code_parts = [consolidated_imports_code]
    for function_file_name in generated_function_names:
        import_path = function_name_map.get(function_file_name)
        module_name = os.path.splitext(os.path.basename(import_path))[0]
        actual_function_name = function_name_map[function_file_name]
        final_code_parts.append(f"from .{os.path.dirname(import_path).replace('/', '.')}.{module_name} import {actual_function_name}")
    for template_file_name in generated_template_names:
        import_path = template_name_map.get(template_file_name)
        module_name = os.path.splitext(os.path.basename(import_path))[0]
        actual_template_var_name = template_name_map[template_file_name]
        final_code_parts.append(f"from .{os.path.dirname(import_path).replace('/', '.')}.{module_name} import {actual_template_var_name}")

    final_code_parts.append(step_definitions_code)
    final_code_parts.append(main_graph_code)

    final_code = "\n\n".join(final_code_parts)
    write_file(graph_file_name, final_code)

    return final_code, function_name_map, template_name_map

def _generate_graph_code_recursive(schema: Dict[str, Any], generated_function_names: Set[str] = None, collected_import_lines: Set[str] = None, generated_template_names: Set[str] = None) -> Tuple[Dict[str, str], str, str, Set[str], Dict[str, str], Set[str], Set[str], Dict[str, str], Dict[str, str]]: # Return name_maps
    """
    Recursively generates code components for a StepGraph and its subgraphs, referencing LLM client definitions.
    Returns code components along with sets of generated function and template names.

    Args:
        schema (Dict[str, Any]): Schema for the current graph level.
        generated_function_names (Set[str], optional): Set to track function file names (for de-duplication).
        collected_import_lines (Set[str], optional): Set to accumulate import lines.
        generated_template_names (Set[str], optional): Set to track template file names (for de-duplication).

    Returns:
        Tuple[Dict[str, str], str, str, Set[str], Dict[str, str], Set[str], Set[str], Dict[str, str], Dict[str, str]]: Function definitions, step definitions,
                                                 main graph code, collected import lines, template definitions,
                                                 generated function file names, generated template file names, function name map, template name map
    """
    if generated_function_names is None:
        generated_function_names = set()
    if collected_import_lines is None:
        collected_import_lines = set()
    if generated_template_names is None:
        generated_template_names = set()

    function_name_map: Dict[str, str] = {}
    template_name_map: Dict[str, str] = {}

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
    function_definitions_code: Dict[str, str] = {}
    template_definitions_code: Dict[str, str] = {}

    collected_import_lines.update([
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
                function_file_name = f"{graph_name.replace(' ', '_').replace('-', '_').replace('.', '_')}_{function_ref}_function"
                if function_file_name not in generated_function_names:
                    function_code_content = f"""\
from typing import Any, Dict

def {function_ref}(inputs: Dict[str, Any]) -> Dict[str, Any]:
    pass
    # END_OF_FUNCTION
"""
                    function_definitions_code[function_file_name] = function_code_content
                    generated_function_names.add(function_file_name)
                    function_name_map[function_file_name] = function_ref

                step_instantiation = f"""\
    {step_name} = Step(
        step_name='{step_name}',
        required_inputs={required_inputs_step},
        required_outputs={required_outputs_step},
        function={function_ref},
    )
"""
                immediate_step_definitions.append(step_instantiation)
            elif llm_client:
                template_var_name = f"{step_name.replace(' ', '_').replace('-', '_').replace('.', '_')}_template"
                template_file_name = f"{graph_name.replace(' ', '_').replace('-', '_').replace('.', '_')}_{template_var_name}"
                if template_file_name not in generated_template_names:
                    template_code_content = f"""\
{template_var_name} = f\"\"\"
# Define your template string for step: {step_name} here
\"\"\"
"""
                    template_definitions_code[template_file_name] = template_code_content
                    generated_template_names.add(template_file_name)
                    template_name_map[template_file_name] = template_var_name

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
                function_file_name = f"{graph_name.replace(' ', '_').replace('-', '_').replace('.', '_')}_{fan_out_function_ref}_function"

                if function_file_name not in generated_function_names:
                    function_code_content = f"""\
from typing import Any, Dict

def {fan_out_function_ref}(item: Any, inputs: Dict[str, Any]) -> Dict[str, Any]:
    \"\"\"
    Placeholder function for fan-out step: {step_name}
    Implement your function logic here.
    \"\"\"
    pass
    # END_OF_FUNCTION
"""
                    function_definitions_code[function_file_name] = function_code_content
                    generated_function_names.add(function_file_name)
                    function_name_map[function_file_name] = fan_out_function_ref


                step_instantiation = f"""\
    {step_name} = FanOutStep(
        step_name='{step_name}',
        required_inputs={required_inputs_step},
        required_outputs={required_outputs_step},
        input_key='{input_key}',
        output_key='{output_key}',
        function={fan_out_function_ref},
        concurrency={concurrency},
        batch_mode={batch_mode},
    )
"""
                immediate_step_definitions.append(step_instantiation)
            elif llm_client:
                template_var_name = f"{step_name.replace(' ', '_').replace('-', '_').replace('.', '_')}_template"
                template_file_name = f"{graph_name.replace(' ', '_').replace('-', '_').replace('.', '_')}_{template_var_name}"

                if template_file_name not in generated_template_names:
                    template_code_content = f"""\
{template_var_name} = f\"\"\" # Define your template string for fan-out step: {step_name} here
\"\"\"
"""
                    template_definitions_code[template_file_name] = template_code_content
                    generated_template_names.add(template_file_name)
                    template_name_map[template_file_name] = template_var_name

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
                immediate_step_definitions.append(step_instantiation)
            elif step_graph_ref:
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
                deferred_step_definitions[step_name] = {'code_blob': step_instantiation, 'depends_on': [step_graph_ref]}

        elif step_type == "ConditionalRouterStep":
            steps_config = step_config.get("steps")
            default_step_ref = step_config.get("default")

            steps_route_map_code = "{"
            route_steps = []
            depends_on_steps = []
            for route_key, route_step_name in steps_config.items():
                step_ref_name = route_step_name.get('step_name')
                if step_ref_name:
                    route_steps.append(f"'{route_key}': {step_ref_name}")
                    depends_on_steps.append(step_ref_name)
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
            deferred_step_definitions[step_name] = {'code_blob': step_instantiation, 'depends_on': depends_on_steps}

        elif step_type == "StepGraph":
            subgraph_step_name = step_name
            subgraph_required_inputs = required_inputs_step
            subgraph_required_outputs = required_outputs_step

            sub_function_defs, sub_step_defs, sub_main_graph_code, sub_imports, sub_template_defs, sub_generated_function_names, sub_generated_template_names, sub_function_name_map, sub_template_name_map = _generate_graph_code_recursive(
                schema={ "configuration": step_config, "graph_name": subgraph_step_name, "required_inputs": subgraph_required_inputs, "required_outputs": subgraph_required_outputs, "llm_clients": llm_clients_schema},
                generated_function_names=generated_function_names,
                collected_import_lines=collected_import_lines,
                generated_template_names=generated_template_names,
            )
            function_definitions_code.update(sub_function_defs)
            template_definitions_code.update(sub_template_defs)
            step_definitions_code += sub_step_defs
            step_definitions_code += f"\n{sub_main_graph_code}\n"
            collected_import_lines.update(sub_imports)
            generated_function_names.update(sub_generated_function_names)
            generated_template_names.update(sub_generated_template_names)
            function_name_map.update(sub_function_name_map)
            template_name_map.update(sub_template_name_map)


            subgraph_function_name = f"build_{subgraph_step_name.replace(' ', '_').replace('-', '_').replace('.', '_')}_graph"
            step_instantiation = f"    {step_name} = {subgraph_function_name}()\n"
            deferred_step_definitions[step_name] = {'code_blob': step_instantiation, 'depends_on': []}

        else:
            raise ValueError(f"Unknown step type: {step_type}")

    step_instantiations_code += "".join(immediate_step_definitions)

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
    return function_definitions_code, step_definitions_code, main_graph_code, collected_import_lines, template_definitions_code, generated_function_names, generated_template_names, function_name_map, template_name_map

def _consolidate_imports_to_string(import_lines: Set[str]) -> str:
    return "\n".join(sorted(list(import_lines))) + "\n\n"
