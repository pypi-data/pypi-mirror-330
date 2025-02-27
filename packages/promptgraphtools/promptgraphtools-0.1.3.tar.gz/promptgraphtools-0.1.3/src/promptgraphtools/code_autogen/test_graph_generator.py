from graph_generator import generate_graph_code, get_function_code, get_template_code, set_function_code, set_template_code

example_schema = {
    "graph_name": "MutateFileGraph",
    "required_inputs": [
        "codebase_hierarchy",
        "file_contents"
    ],
    "required_outputs": [
        "mutations_per_filepath"
    ],
    "llm_clients": {
        "gemini_client": {
            "model": "gemini-2-0-flash-thinking",
            "max_output_tokens": 8000,
            "temperature": 0.1,
            "top_p": 0.95,
            "use_tools": True
        },
        "gemini_client_for_verify": {
            "model": "gemini-2-0-flash-thinking",
            "max_output_tokens": 8000,
            "temperature": 0.1,
            "top_p": 0.95,
            "use_tools": True
        }
    },
    "configuration": {
        "steps": [
            {
                "step_name": "SummaryVerifyGraph",
                "step_type": "StepGraph",
                "required_inputs": [
                    "codebase_hierarchy",
                    "file_contents"
                ],
                "required_outputs": [
                    "verified_generation"
                ],
                "configuration": {
                    "steps": [
                        {
                            "step_name": "FileSummaryStep",
                            "step_type": "ConditionalRouterStep",
                            "required_inputs": [
                                "inputs",
                                "file_contents"
                            ],
                            "required_outputs": [
                                "code_transformation_plan"
                            ],
                            "configuration": {
                                "steps": {
                                    "existing_code_transformation_plan": {
                                        "step_name": "FileSummaryStep__WithIssuesRepairContext"
                                    }
                                },
                                "default": "FileSummaryStep__InitialGeneration"
                            }
                        },
                        {
                            "step_name": "FileSummaryStep__InitialGeneration",
                            "step_type": "Step",
                            "required_inputs": [
                                "inputs",
                                "file_contents"
                            ],
                            "required_outputs": [
                                "code_transformation_plan"
                            ],
                            "configuration": {
                                "llm_client": "gemini_client"
                            }
                        },
                        {
                            "step_name": "FileSummaryStep__WithIssuesRepairContext",
                            "step_type": "Step",
                            "required_inputs": [
                                "inputs",
                                "file_contents",
                                "existing_code_transformation_plan"
                            ],
                            "required_outputs": [
                                "code_transformation_plan"
                            ],
                            "configuration": {
                                "llm_client": "gemini_client"
                            }
                        },
                        {
                            "step_name": "VerifyFileSummaryMultiFile",
                            "step_type": "Step",
                            "required_inputs": [
                                "code_transformation_plan",
                                "file_summaries"
                            ],
                            "required_outputs": [
                                "verify_generation_output"
                            ],
                            "configuration": {
                                "llm_client": "gemini_client_for_verify"
                            }
                        },
                        {
                            "step_name": "VerifyOutputFormatterStep",
                            "step_type": "Step",
                            "required_inputs": [
                                "verify_generation_output"
                            ],
                            "required_outputs": [
                                "verified_generation"
                            ],
                            "configuration": {
                                "function": "._format_verify_output"
                            }
                        }
                    ],
                    "dependencies": {
                        "FileSummaryStep": [], # No dependencies for ConditionalRouterStep itself
                        "VerifyFileSummaryMultiFile": [
                            "FileSummaryStep" # Verify depends on the output of FileSummaryStep
                        ],
                        "VerifyOutputFormatterStep": [
                            "VerifyFileSummaryMultiFile" # Formatter depends on Verify
                        ]
                    }
                }
            },
            {
                "step_name": "MutationsGraph",
                "step_type": "StepGraph",
                "required_inputs": [
                    "verified_generation"
                ],
                "required_outputs": [
                    "mutations_per_filepath"
                ],
                "configuration": {
                    "steps": [
                        {
                            "step_name": "ExtractFilepathsStep",
                            "step_type": "Step",
                            "required_inputs": [
                                "inputs",
                                "file_contents",
                                "codebase_hierarchy",
                                "verified_generation"
                            ],
                            "required_outputs": [
                                "filepaths_generation"
                            ],
                            "configuration": {
                                "llm_client": "gemini_client"
                            }
                        },
                        {
                            "step_name": "ExtractFilepathsOutputFormatterStep",
                            "step_type": "Step",
                            "required_inputs": [
                                "filepaths_generation"
                            ],
                            "required_outputs": [
                                "formatted_filepaths"
                            ],
                            "configuration": {
                                "function": "._format_filepaths_output"
                            }
                        },
                        {
                            "step_name": "GenerateMutationsStep",
                            "step_type": "FanOutStep",
                            "required_inputs": [
                                "formatted_filepaths"
                            ],
                            "required_outputs": [
                                "mutations_per_filepath"
                            ],
                            "configuration": {
                                "input_key": "formatted_filepaths",
                                "output_key": "mutations_per_filepath",
                                "step_graph": "MutateFileContinuationGraph"
                            }
                        }
                    ],
                    "dependencies": {
                        "ExtractFilepathsStep": [], # ExtractFilepathsStep is an entry point
                        "ExtractFilepathsOutputFormatterStep": [
                            "ExtractFilepathsStep" # Output formatter depends on filepath extraction
                        ],
                        "GenerateMutationsStep": [
                            "ExtractFilepathsOutputFormatterStep" # Generate Mutations depends on formatted filepaths
                        ]
                    }
                }
            },
            {
                "step_name": "MutateFileContinuationGraph",
                "step_type": "StepGraph",
                "required_inputs": [
                    "dynamic_input"
                ],
                "required_outputs": [
                    "mutate_file_generation"
                ],
                "configuration": {
                    "steps": [
                        {
                            "step_name": "MutateFileStep",
                            "step_type": "Step",
                            "required_inputs": [
                                "dynamic_input"
                            ],
                            "required_outputs": [
                                "mutate_file_generation"
                            ],
                            "configuration": {
                                "llm_client": "gemini_client"
                            }
                        }
                    ],
                    "dependencies": {
                        "MutateFileStep": [] # No dependencies for MutateFileStep
                    }
                }
            }
        ],
        "dependencies": {
            "SummaryVerifyGraph": [], # SummaryVerifyGraph is an entry point
            "MutationsGraph": ["SummaryVerifyGraph"], # MutationsGraph depends on the output of SummaryVerifyGraph
            "MutateFileContinuationGraph": [] # MutateFileContinuationGraph is used internally in FanOutStep, not directly in MutateFileGraph's main steps
        }
    }
}

generated_code, function_names, template_names = generate_graph_code(example_schema)
print(generated_code, "\n\n", function_names, "\n\n", template_names)

# print("\n\n\n\n\n\n\n\n")

# generated_code, function_names, template_names = generate_graph_code(example_schema)
# print("Generated Code:\n", generated_code)
# print("\nGenerated Function Names:", function_names)
# print("Generated Template Names:", template_names)

# # Example of using getter and setter functions:
# function_to_get = "_summarize_files"
# function_code = get_function_code(generated_code, function_to_get)
# if function_code:
#     print(f"\n--- Code for function '{function_to_get}': ---\n{function_code}")

# template_to_get = "VerifyFileSummaryMultiFile_template"
# template_content = get_template_code(generated_code, template_to_get)
# if template_content:
#     print(f"\n--- Content for template '{template_to_get}': ---\n{template_content}")

# new_function_code = """def _summarize_files(inputs: Dict[str, Any]) -> Dict[str, Any]:
# \"\"\"
# This is a modified function.
# \"\"\"
# return {"file_summary_output": "Summarized content"}
# # END_OF_FUNCTION
# """
# modified_code_with_function = set_function_code(generated_code, function_to_get, new_function_code)
# print(f"\n--- Modified Code with new function '{function_to_get}': ---\n{get_function_code(modified_code_with_function, function_to_get)}")


# new_template_content = """
# This is a modified template.
# It should now have different content.
# """
# modified_code_with_template = set_template_code(generated_code, template_to_get, new_template_content)
# print(f"\n--- Modified Code with new template '{template_to_get}': ---\n{get_template_code(modified_code_with_template, template_to_get)}")
