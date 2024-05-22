from fastapi import FastAPI, HTTPException, File, UploadFile, Form
from typing import List, Dict, Any
from fastapi.middleware.cors import CORSMiddleware
from llama_index.question_gen.openai import OpenAIQuestionGenerator
from llama_index.core.tools import ToolMetadata
from llama_index.core import QueryBundle
import logging
import json
from openaicall import chat_completion_request
from functions import custom_functions
from utils import *

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

app = FastAPI()

# Allow CORS for all origins (not recommended for production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

conversation_history: List[Dict[str, Any]] = []

@app.post("/process_request")
async def process_request(user_request: str = Form(...), file: UploadFile = File(...)):
    global conversation_history

    try:
        sample_data = json.loads(await file.read())
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid JSON file: {e}")

    prompt = f"""
    Given the following JSON data:

    {json.dumps(sample_data, indent=2)}

    Please analyze the provided JSON data and perform one of the following tasks:

    1. If the user requests project information, call the `extract_project_info` function and provide the necessary details.
    2. If the user requests task information for a specific task ID, call the `extract_task_info` function and provide the necessary details for that task.
    3. If the user requests a project risk assessment, call the `assess_project_risks` function and provide a detailed risk assessment based on the critical path tasks and their completion status.
    4. If the user requests information about allocated resources, call the `resource_allocation_info` function and provide the details of the allocated resources.
    5. If the user requests tasks with a specific completion rate or range, call the `tasks_with_completion_rate` function and provide the matching tasks.
    6. If the user requests task reassignments to help team members with low completion rates, call the `allocate_resources` function and provide the allocation suggestions.
    7. If the user's request doesn't match any of the above scenarios, provide a relevant response based on the conversation context.

    Select the appropriate function based on the user's request and input data. Provide specific and detailed information in the response.

    Conversation History:
    {conversation_history}

    User Request: {user_request}
    """

    response = chat_completion_request(
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": user_request}
        ],
        tools=custom_functions,
        function_call="auto"
    )

    if isinstance(response, Exception):
        result = "An error occurred: " + str(response)
    else:
        if hasattr(response, 'choices') and response.choices:
            response_message = response.choices[0].message

            if hasattr(response_message, 'function_call') and response_message.function_call:
                function_name = response_message.function_call.name
                function_args = json.loads(response_message.function_call.arguments)

                if function_name == "extract_project_info":
                    result = extract_project_info(**function_args)
                elif function_name == "extract_task_info":
                    result = extract_task_info(**function_args)
                elif function_name == "assess_project_risks":
                    result = assess_project_risks(
                        function_args['PROJECT_CRITICAL_PATH_TASKS'],
                        sample_data['TASKS'],
                        sample_data['PROJECT_SKILLS_REQUIRED'],
                        sample_data['RESOURCE_ALLOCATED'],
                        sample_data['PROJECT_DURATION'],
                        sample_data['PROJECT_START_DATE'],
                        sample_data['PROJECT_END_DATE'],
                        sample_data['PROJECT_ADJ_END_DATE'],
                        sample_data['PROJECT_COST']
                    )
                elif function_name == "resource_allocation_info":
                    result = resource_allocation_info(**function_args)
                elif function_name == "tasks_with_completion_rate":
                    result = tasks_with_completion_rate(sample_data['TASKS'], function_args['completion_rate'])
                elif function_name == "allocate_resources":
                    result = allocate_resources(sample_data['TASKS'], sample_data['RESOURCE_ALLOCATED'], sample_data['PROJECT_SKILLS_REQUIRED'])
                else:
                    result = "Unsupported function called."
            else:
                result = response_message.content
        else:
            result = "Unexpected response format."

    # Generate sub-questions
    tools = [
        ToolMetadata(
            name="extract_project_info",
            description="Provides project information",
        ),
        ToolMetadata(
            name="extract_task_info",
            description="Provides task information for a specific task ID",
        ),
        ToolMetadata(
            name="assess_project_risks",
            description="Provides a detailed project risk assessment",
        ),
        ToolMetadata(
            name="resource_allocation_info",
            description="Provides information about allocated resources",
        ),
        ToolMetadata(
            name="tasks_with_completion_rate",
            description="Provides tasks with a specific completion rate or range",
        ),
        ToolMetadata(
            name="allocate_resources",
            description="Suggests task reassignments to help team members with low completion rates",
        ),
    ]

    question_gen = OpenAIQuestionGenerator.from_defaults()
    sub_questions = question_gen.generate(
        tools=tools,
        query=QueryBundle(user_request),
    )

    conversation_history.append({"user": user_request, "assistant": result})

    return {"result": result, "sub_questions": sub_questions, "conversation_history": conversation_history}