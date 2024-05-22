import json
from datetime import datetime


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