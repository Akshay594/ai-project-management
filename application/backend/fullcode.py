import os
import json
from openai import OpenAI
from datetime import datetime

API_KEY = os.getenv("API_KEY")
os.environ["OPENAI_API_KEY"] = API_KEY
from tenacity import retry, wait_random_exponential, stop_after_attempt
import logging

client = OpenAI()
logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

@retry(wait=wait_random_exponential(multiplier=1, max=40), stop=stop_after_attempt(3))
def chat_completion_request(messages, tools=None, function_call=None, model="gpt-3.5-turbo"):
    try:
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            functions=tools,
            function_call=function_call
        )
        log.info(f"API response: {response}")
        return response
    except Exception as e:
        log.error("Unable to generate ChatCompletion response")
        log.error(f"Exception: {e}")
        return e
import json

def extract_project_info(PROJECT_ID, PROJECT_NAME, PROJECT_DESCRIPTION, PROJECT_START_DATE, PROJECT_END_DATE):
    start_date = datetime.strptime(PROJECT_START_DATE, "%Y-%m-%d")
    end_date = datetime.strptime(PROJECT_END_DATE, "%Y-%m-%d")
    duration = (end_date - start_date).days
    
    response = {
        "project_id": PROJECT_ID,
        "project_name": PROJECT_NAME,
        "project_description": PROJECT_DESCRIPTION,
        "start_date": PROJECT_START_DATE,
        "end_date": PROJECT_END_DATE,
        "duration": duration
    }
    
    return json.dumps(response, indent=2)
    

def extract_task_info(task_id, task_name, task_description, skill, completion_percentage, start_date, end_date):
    response = {
        "task_id": task_id,
        "task_name": task_name,
        "task_description": task_description,
        "skill": skill,
        "completion_percentage": completion_percentage,
        "start_date": start_date,
        "end_date": end_date
    }
    
    return json.dumps(response, indent=2)


def tasks_with_completion_rate(tasks, completion_rate):
    rate = float(completion_rate.strip('%')) / 100.0
    tasks_with_completion = [(task, float(task["completion_percentage"])) for task in tasks]
    tasks_with_completion.sort(key=lambda x: abs(x[1] - rate * 100))
    
    closest_rate_tasks = [task for task, completion in tasks_with_completion if completion == tasks_with_completion[0][1]]
    
    if not closest_rate_tasks:
        return "No tasks found with the specified completion rate or range."
    
    return json.dumps(closest_rate_tasks, indent=2)
    

def assess_project_risks(PROJECT_CRITICAL_PATH_TASKS, TASKS, PROJECT_SKILLS_REQUIRED, RESOURCE_ALLOCATED, PROJECT_DURATION, PROJECT_START_DATE, PROJECT_END_DATE, PROJECT_ADJ_END_DATE, PROJECT_COST):
    risks = []

    # Resource Skill Gaps
    for resource in RESOURCE_ALLOCATED:
        resource_skills = [skill['skill_name'] for skill in PROJECT_SKILLS_REQUIRED if skill['count'] > 0]
        if len(resource_skills) > 1:
            risks.append({
                "category": "Resource Skill Gaps",
                "description": f"{resource['resource_name']} is allocated {', '.join(resource_skills)} tasks. If these types of tasks overlap or require simultaneous attention, {resource['resource_name']} might face overload."
            })

    # Project Duration and Task Dependencies
    risks.append({
        "category": "Project Duration and Task Dependencies",
        "description": f"The project is scheduled for {PROJECT_DURATION} days, starting on {PROJECT_START_DATE} and ending on {PROJECT_END_DATE}, with an adjusted end date of {PROJECT_ADJ_END_DATE}. The close proximity of the adjusted end date suggests there is very little buffer for delays."
    })

    dependent_tasks = [task for task in TASKS if task.get('task_dependencies')]
    if len(dependent_tasks) < len(TASKS):
        risks.append({
            "category": "Project Duration and Task Dependencies",
            "description": "Not all tasks have their dependencies listed. Ensuring all tasks and their dependencies are comprehensively mapped is crucial to avoid bottlenecks."
        })

    # Task Completion and Monitoring
    ongoing_tasks = [task for task in TASKS if int(task['completion_percentage']) < 100]
    for task in ongoing_tasks:
        risks.append({
            "category": "Task Completion and Monitoring",
            "description": f"{task['task_name']} is {task['completion_percentage']}% complete. Monitoring its progress is essential to avoid delays, especially if it is part of the critical path."
        })

    risks.append({
        "category": "Task Completion and Monitoring",
        "description": f"Ensuring that critical path tasks ({', '.join(PROJECT_CRITICAL_PATH_TASKS)}) are closely monitored and completed on time is essential to avoid delays in the overall project timeline."
    })

    # Cost Management
    risks.append({
        "category": "Cost Management",
        "description": f"The project cost is set at ${PROJECT_COST}. Any unforeseen expenses or resource requirements beyond the allocated budget could impact project completion."
    })

    # Scope and Complexity
    risks.append({
        "category": "Scope and Complexity",
        "description": "Developing a comprehensive onboarding system with Okta integration, Terraform infrastructure, React frontend, Python Fast API backend, and Figma designs within the given timeline may present challenges in terms of coordination and integration of different components."
    })

    # Quality Assurance
    qa_resources = [resource for resource in RESOURCE_ALLOCATED if 'QA' in resource.get('skills', [])]
    if len(qa_resources) == 1:
        risks.append({
            "category": "Quality Assurance",
            "description": f"{qa_resources[0]['resource_name']} is the only QA resource. This could be a bottleneck during the testing phase, especially if multiple components require simultaneous testing."
        })

    mitigation_actions = [
        "Reevaluate resource allocation and possibly bring in additional resources or provide cross-training.",
        "Ensure detailed task breakdown and dependencies for all project phases.",
        "Implement robust project monitoring and reporting mechanisms to track progress and address issues promptly.",
        "Establish contingency plans for potential delays or resource unavailability.",
        "Regularly review and adjust the project plan to accommodate any changes or emerging risks."
    ]

    response = {
        "risks": risks,
        "mitigation_actions": mitigation_actions
    }

    return json.dumps(response, indent=2)

    


def resource_allocation_info(RESOURCE_ALLOCATED):
    resources = []
    for resource in RESOURCE_ALLOCATED:
        resources.append({
            "resource_name": resource['resource_name'],
            "resource_id": resource['resource_id']
        })
    
    response = {
        "resource_allocation": resources
    }
    
    return json.dumps(response, indent=2)

# def allocate_resources(tasks, resources, completion_threshold=30):
#     # Calculate completion percentage for each resource
#     resource_completion = {}
#     for resource in resources:
#         resource_tasks = [task for task in tasks if task['skill'] in resource['skills']]
#         completed_tasks = [task for task in resource_tasks if float(task['completion_percentage']) == 100]
#         resource_completion[resource['resource_id']] = len(completed_tasks) / len(resource_tasks) if resource_tasks else 0

#     # Find resources with completion percentage above the threshold
#     available_resources = [resource for resource in resources if resource_completion[resource['resource_id']] * 100 >= completion_threshold]

#     # Find tasks with completion percentage below the threshold
#     tasks_needing_help = [task for task in tasks if float(task['completion_percentage']) < completion_threshold]

#     allocation_suggestions = []
#     for task in tasks_needing_help:
#         eligible_resources = [resource for resource in available_resources if task['skill'] in resource['skills']]
#         if eligible_resources:
#             allocated_resource = max(eligible_resources, key=lambda resource: resource_completion[resource['resource_id']])
#             allocation_suggestions.append({
#                 'task': task['task_id'],
#                 'resource': allocated_resource['resource_id']
#             })

#     if not allocation_suggestions:
#         return "No allocation suggestions available at the moment."

#     return json.dumps({
#         'allocation_suggestions': allocation_suggestions
#     }, indent=2)

def allocate_resources(tasks, resources, completion_threshold=30):
    # Calculate completion percentage for each resource
    resource_completion = {}
    for resource in resources:
        resource_tasks = [task for task in tasks if task['skill'] in resource['skills']]
        completed_tasks = [task for task in resource_tasks if float(task['completion_percentage']) == 100]
        resource_completion[resource['resource_id']] = len(completed_tasks) / len(resource_tasks) if resource_tasks else 0

    # Find resources with completion percentage above the threshold
    available_resources = [resource for resource in resources if resource_completion[resource['resource_id']] * 100 >= completion_threshold]

    # Find tasks with completion percentage below the threshold
    tasks_needing_help = [task for task in tasks if float(task['completion_percentage']) < completion_threshold]

    allocation_suggestions = []
    for task in tasks_needing_help:
        eligible_resources = [resource for resource in available_resources if task['skill'] in resource['skills']]
        if eligible_resources:
            allocated_resource = max(eligible_resources, key=lambda resource: resource_completion[resource['resource_id']])
            allocation_suggestions.append({
                'task': task['task_id'],
                'resource': allocated_resource['resource_id']
            })
            
            # Update the sample data to reflect the allocation
            task['allocated_resource'] = allocated_resource['resource_id']

    if not allocation_suggestions:
        return "No allocation suggestions available at the moment."

    return json.dumps({
        'allocation_suggestions': allocation_suggestions
    }, indent=2)


custom_functions = [
    {
        "name": "extract_project_info",
        "description": "Extract project information from the input data",
        "parameters": {
            "type": "object",
            "properties": {
                "PROJECT_ID": {"type": "string"},
                "PROJECT_NAME": {"type": "string"},
                "PROJECT_DESCRIPTION": {"type": "string"},
                "PROJECT_START_DATE": {"type": "string"},
                "PROJECT_END_DATE": {"type": "string"}
            },
            "required": ["PROJECT_ID", "PROJECT_NAME", "PROJECT_DESCRIPTION", "PROJECT_START_DATE", "PROJECT_END_DATE"]
        }
    },
    {
        "name": "extract_task_info",
        "description": "Extract task information from the input data",
        "parameters": {
            "type": "object",
            "properties": {
                "task_id": {"type": "string"},
                "task_name": {"type": "string"},
                "task_description": {"type": "string"},
                "skill": {"type": "string"},
                "completion_percentage": {"type": "string"},
                "start_date": {"type": "string"},
                "end_date": {"type": "string"}
            },
            "required": ["task_id", "task_name", "task_description", "skill", "completion_percentage", "start_date", "end_date"]
        }
    },
    {
        "name": "assess_project_risks",
        "description": "Assess project risks based on critical path tasks and their completion status",
        "parameters": {
            "type": "object",
            "properties": {
                "PROJECT_CRITICAL_PATH_TASKS": {"type": "array", "items": {"type": "string"}},
                "TASKS": {"type": "array", "items": {"type": "object"}},
                "PROJECT_SKILLS_REQUIRED": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "skill_name": {"type": "string"},
                            "count": {"type": "integer"}
                        },
                        "required": ["skill_name", "count"]
                    }
                },
                "RESOURCE_ALLOCATED": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "resource_name": {"type": "string"},
                            "resource_id": {"type": "integer"}
                        },
                        "required": ["resource_name", "resource_id"]
                    }
                },
                "PROJECT_DURATION": {"type": "integer"},
                "PROJECT_START_DATE": {"type": "string"},
                "PROJECT_END_DATE": {"type": "string"},
                "PROJECT_ADJ_END_DATE": {"type": "string"},
                "PROJECT_COST": {"type": "number"}
            },
            "required": [
                "PROJECT_CRITICAL_PATH_TASKS",
                "TASKS",
                "PROJECT_SKILLS_REQUIRED",
                "RESOURCE_ALLOCATED",
                "PROJECT_DURATION",
                "PROJECT_START_DATE",
                "PROJECT_END_DATE",
                "PROJECT_ADJ_END_DATE",
                "PROJECT_COST"
            ]
        }
    },
    {
        "name": "resource_allocation_info",
        "description": "Provide information about allocated resources",
        "parameters": {
            "type": "object",
            "properties": {
                "RESOURCE_ALLOCATED": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "resource_name": {"type": "string"},
                            "resource_id": {"type": "integer"}
                        },
                        "required": ["resource_name", "resource_id"]
                    }
                }
            },
            "required": ["RESOURCE_ALLOCATED"]
        }
    },
    {
        "name": "tasks_with_completion_rate",
        "description": "Retrieve tasks with completion percentage less than or equal to the specified rate",
        "parameters": {
            "type": "object",
            "properties": {
                "tasks": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "task_id": {"type": "string"},
                            "task_name": {"type": "string"},
                            "skill": {"type": "string"},
                            "completion_percentage": {"type": "string"},
                            "task_description": {"type": "string"},
                            "duration_days": {"type": "integer"},
                            "start_date": {"type": "string"},
                            "end_date": {"type": "string"},
                            "task_dependencies": {
                                "type": "array",
                                "items": {"type": "string"}
                            }
                        },
                        "required": ["task_id", "task_name", "skill", "completion_percentage", "task_description", "duration_days", "start_date", "end_date", "task_dependencies"]
                    }
                },
                "completion_rate": {"type": "string"}
            },
            "required": ["tasks", "completion_rate"]
        }
    },

    {
        "name": "allocate_resources",
        "description": "Suggest task reassignments based on completion percentage",
        "parameters": {
            "type": "object",
            "properties": {
                "tasks": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "task_id": {"type": "string"},
                            "task_name": {"type": "string"},
                            "skill": {"type": "string"},
                            "completion_percentage": {"type": "string"}
                        },
                        "required": ["task_id", "task_name", "skill", "completion_percentage"]
                    }
                },
                "resources": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "resource_id": {"type": "integer"},
                            "resource_name": {"type": "string"},
                            "skills": {
                                "type": "array",
                                "items": {"type": "string"}
                            }
                        },
                        "required": ["resource_id", "resource_name", "skills"]
                    }
                }
            },
            "required": ["tasks", "resources"]
        }
    }
]
sample_data = json.loads('''
{
    "PROJECT_ID": "cbe96293-f9e5-4d8e-8e33-b92c14a4ea4f",
    "PROJECT_NAME": "Test with Francois",
    "PROJECT_DESCRIPTION": "Create a detailed project management plan for onboarding. We are going to use Okta for authentication and MFA. We use terraform for infrastructure, the front end is built in react and the backend is python fast API, design will be done in Figma. Onboarding should have steps like signup, create org, and corporation info.",
    "PROJECT_DURATION": 27,
    "PROJECT_START_DATE": "2024-05-11",
    "PROJECT_END_DATE": "2024-06-11",
    "PROJECT_ADJ_END_DATE": "2024-06-22",
    "PROJECT_COST": 15480.0,
    "PROJECT_CRITICAL_PATH_TASKS": [
        "sim_1",
        "sim_2",
        "sim_4",
        "sim_5",
        "sim_6",
        "sim_7"
    ],
    "PROJECT_SKILLS_REQUIRED": [
        {
            "skill_name": "DEVOPS",
            "count": 1
        },
        {
            "skill_name": "BACKEND",
            "count": 1
        },
        {
            "skill_name": "FRONTEND",
            "count": 1
        },
        {
            "skill_name": "QA",
            "count": 1
        },
        {
            "skill_name": "UIDESIGN",
            "count": 1
        },
        {
            "skill_name": "UXDESIGN",
            "count": 1
        }
    ],
    "RESOURCE_ALLOCATED": [
        {
            "resource_name": "dummy_resource_4",
            "resource_id": 71
        },
        {
            "resource_name": "dummy_resource_6",
            "resource_id": 73
        },
        {
            "resource_name": "dummy_resource_1",
            "resource_id": 68
        }
    ],
    "TASKS": [
        {
            "task_id": "sim_1",
            "task_name": "Setup Okta for Authentication and MFA",
            "skill": "DEVOPS",
            "completion_percentage": "15",
            "task_description": "Setup an Okta account, configure the necessary settings for the onboarding process. This includes setting up the authentication, MFA, users, and groups. Ensure that appropriate security measures are in place. It is recommended that you follow Okta's best practices for setting this up.",
            "duration_days": 3,
            "start_date": "2024-05-15",
            "end_date": "2024-05-18",
            "task_dependencies": []
        },
        {
            "task_id": "sim_2",
            "task_name": "Setup Terraform Infrastructure",
            "skill": "DEVOPS",
            "completion_percentage": "0",
            "task_description": "Using Terraform, setup the required infrastructure for the onboarding process. This includes setting up servers, databases, and other necessary services. Ensure that everything is properly linked and secure. Be sure to follow Terraform's best practices when setting this up.",
            "duration_days": 5,
            "start_date": "2024-05-18",
            "end_date": "2024-05-23",
            "task_dependencies": [
                "sim_1"
            ]
        },
        {
            "task_id": "sim_4",
            "task_name": "Implement Backend with Python Fast API",
            "skill": "BACKEND",
            "completion_percentage": "0",
            "task_description": "Using Python Fast API, implement the backend for the onboarding process. This includes setting up the necessary endpoints for signup, creating organizations, and entering corporation information. Make sure to properly integrate with Okta for authentication and MFA. Also, ensure that all data is properly stored and retrieved from the database.",
            "duration_days": 7,
            "start_date": "2024-05-23",
            "end_date": "2024-05-30",
            "task_dependencies": [
                "sim_2"
            ]
        },
        {
            "task_id": "sim_5",
            "task_name": "Implement Frontend in React",
            "skill": "FRONTEND",
            "completion_percentage": "0",
            "task_description": "Using React, implement the frontend for the onboarding process based on the design created in Figma. Make sure to properly connect with the backend using the endpoints created. Also, integrate with Okta for the authentication and MFA. Ensure that the user experience is smooth and intuitive.",
            "duration_days": 7,
            "start_date": "2024-05-30",
            "end_date": "2024-06-06",
            "task_dependencies": [
                "sim_3",
                "sim_4"
            ]
        },
        {
            "task_id": "sim_6",
            "task_name": "Perform QA Testing",
            "skill": "QA",
            "completion_percentage": "0",
            "task_description": "Perform quality assurance testing on the onboarding process. This includes testing the signup process, creating an organization, and entering corporation information. Ensure that everything works as expected and fix any bugs found. Also, test the authentication and MFA to make sure it's secure and works correctly.",
            "duration_days": 3,
            "start_date": "2024-06-06",
            "end_date": "2024-06-09",
            "task_dependencies": [
                "sim_5"
            ]
        },
        {
            "task_id": "sim_7",
            "task_name": "Deploy Onboarding System",
            "skill": "DEVOPS",
            "completion_percentage": "0",
            "task_description": "Once everything has been tested and is working fine, deploy the onboarding system. Make sure that the deployment process is smooth and that the deployed system works as expected. Monitor the system for any issues and fix them as necessary.",
            "duration_days": 2,
            "start_date": "2024-06-09",
            "end_date": "2024-06-11",
            "task_dependencies": [
                "sim_6"
            ]
        },
        {
            "task_id": "sim_3",
            "task_name": "Design Onboarding Flow in Figma-UIDESIGN",
            "skill": "UIDESIGN",
            "completion_percentage": "25",
            "task_description": "Using Figma, design the UI/UX for the onboarding process. This includes screens for signup, creating an organization, and entering corporation information. Make sure the design is user-friendly and intuitive. Get feedback from other team members and iterate on the design as necessary.",
            "duration_days": 5,
            "start_date": "2024-05-15",
            "end_date": "2024-05-20",
            "task_dependencies": []
        },
        {
            "task_id": "sim_3_2",
            "task_name": "Design Onboarding Flow in Figma-UXDESIGN",
            "skill": "UXDESIGN",
            "completion_percentage": "0",
            "task_description": "Using Figma, design the UI/UX for the onboarding process. This includes screens for signup, creating an organization, and entering corporation information. Make sure the design is user-friendly and intuitive. Get feedback from other team members and iterate on the design as necessary.",
            "duration_days": 5,
            "start_date": "2024-05-20",
            "end_date": "2024-05-25",
            "task_dependencies": [
                "sim_3"
            ]
        }
    ]
}
''')
prompt = f"""
Given the following JSON data:

{json.dumps(sample_data, indent=2)}

Please analyze the provided JSON data and perform one of the following tasks:

1. If the user requests project information, call the `extract_project_info` function and provide the necessary details.
2. If the user requests task information for a specific task ID, call the `extract_task_info` function and provide the necessary details for that task.
3. If the user requests a project risk assessment, call the `assess_project_risks` function and provide a detailed risk assessment based on the critical path tasks and their completion status.
4. If the user requests information about allocated resources, call the `resource_allocation_info` function and provide the details of the allocated resources.

Select the appropriate function based on the user's request and input data. Provide specific and detailed information in the response.
"""
user_request = "Tell me risk assessment for this project"

response = chat_completion_request(
    messages=[
        {"role": "system", "content": prompt},
        {"role": "user", "content": user_request}
    ],
    tools=custom_functions,
    function_call="auto"
)
if isinstance(response, Exception):
    print("An error occurred:", response)
else:
    response_message = response.choices[0].message

    if response_message.function_call:
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
            result = allocate_resources(sample_data['TASKS'], sample_data['RESOURCE_ALLOCATED'])
        else:
            result = "Unsupported function called."
    else:
        result = response_message.content

    print(result)

 # question_gen = OpenAIQuestionGenerator.from_defaults()
 #    sub_questions = question_gen.generate(
 #        tools=tools,
 #        query=QueryBundle(query),
 #    )

 #    conversation_history.append({"user": user_request, "assistant": result})
 #    return result, sub_questions
!pip install llama-index-question-gen-openai llama-index
from llama_index.question_gen.openai import OpenAIQuestionGenerator
from llama_index.core.tools import ToolMetadata
from llama_index.core import QueryBundle

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

conversation_history = []

def process_user_request(user_request, tools, query):
    global conversation_history

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
        response_message = response.choices[0].message

        if response_message.function_call:
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
                result = allocate_resources(sample_data['TASKS'], sample_data['RESOURCE_ALLOCATED'])
            else:
                result = "Unsupported function called."
        else:
            result = response_message.content

    # Generate sub-questions
    question_gen = OpenAIQuestionGenerator.from_defaults()
    sub_questions = question_gen.generate(
        tools=tools,
        query=QueryBundle(query),
    )

    conversation_history.append({"user": user_request, "assistant": result})
    return result, sub_questions

# Main conversation loop
while True:
    user_request = input("User: ")
    if user_request.lower() in ["bye", "goodbye", "exit", "quit"]:
        print("Assistant: Goodbye! Have a great day.")
        break

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
    query = user_request

    result, sub_questions = process_user_request(user_request, tools, query)
    print("Assistant:", result)
    print("Sub-questions:")
    for sq in sub_questions:
        print(f"- {sq.sub_question} (Tool: {sq.tool_name})")
    print()
%history