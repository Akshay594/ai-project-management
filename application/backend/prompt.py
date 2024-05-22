"""
For setting up the system prompt.
"""
import json


def set_prompt(sample_data):
    """
    For system prompt
    """
    prompt = f"""
    Given the following JSON data:

    {json.dumps(sample_data, indent=2)}

    Please analyze the provided JSON data and
    perform one of the following tasks:

    1. If the user requests project information,
    call the `extract_project_info` function and provide the necessary details.
    2. If the user requests task information for a specific task ID,
    call the `extract_task_info` function and provide the necessary details
    for that task.
    3. If the user requests a project risk assessment, call the
    `assess_project_risks` function and provide a detailed risk assessment
    based on the critical path tasks and their completion status.
    4. If the user requests information about allocated resources, call the
    `resource_allocation_info` function and provide the details of the
    allocated resources.

    Select the appropriate function based on the user's request and input data.
    Provide specific and detailed information in the response.
    """

    return prompt
