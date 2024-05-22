"""
This module contains custom functions for openai calling.
"""
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
            "required": ["PROJECT_ID", "PROJECT_NAME",
                         "PROJECT_DESCRIPTION", "PROJECT_START_DATE",
                         "PROJECT_END_DATE"]
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
            "required": ["task_id", "task_name",
                         "task_description", "skill",
                         "completion_percentage",
                         "start_date", "end_date"]
        }
    },
    {
        "name": "assess_project_risks",
        "description": """Assess project risks based on
        critical path tasks and their completion status""",
        "parameters": {
            "type": "object",
            "properties": {
                "PROJECT_CRITICAL_PATH_TASKS": {"type": "array",
                                                "items": {"type": "string"}},
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
        "description": """Retrieve tasks with completion percentage
        less than or equal to the specified rate""",
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
                        "required": ["task_id", "task_name",
                                     "skill", "completion_percentage",
                                     "task_description", "duration_days",
                                     "start_date", "end_date",
                                     "task_dependencies"]
                    }
                },
                "completion_rate": {"type": "string"}
            },
            "required": ["tasks", "completion_rate"]
        }
    },

    {
        "name": "allocate_resources",
        "description": """Suggest task reassignments
        based on completion percentage""",
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
                        "required": ["task_id", "task_name", "skill",
                                     "completion_percentage"]
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
