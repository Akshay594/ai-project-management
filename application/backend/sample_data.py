import json

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
