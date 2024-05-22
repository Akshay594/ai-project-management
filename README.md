# Project Management Application

This is a Python-based project management application that utilizes OpenAI's language model and function calling capabilities to provide intelligent assistance for managing projects. The application allows users to interact with the system through a conversation-style interface and perform various project management tasks.

## Features

- Extract project information, including project ID, name, description, start date, end date, and duration.
- Extract task information for a specific task ID, including task ID, name, description, skill, completion percentage, start date, and end date.
- Perform project risk assessment based on critical path tasks and their completion status.
- Provide information about allocated resources.
- Retrieve tasks with a specific completion rate or range.
- Suggest task reassignments to help team members with low completion rates.
- Generate sub-questions related to the user's query using the OpenAI Question Generator.

## Prerequisites

Before running the application, make sure you have the following:

- Python 3.x installed
- OpenAI API key
- Required Python packages: `openai`, `tenacity`, `llama-index`, `llama-index-question-gen-openai`

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/project-management-app.git
   ```

2. Install the required Python packages:

   ```bash
   pip install openai tenacity llama-index llama-index-question-gen-openai
   ```

3. Set up your OpenAI API key:

   - Create a file named `.env` in the project directory.
   - Add the following line to the `.env` file, replacing `YOUR_API_KEY` with your actual OpenAI API key:

     ```
     API_KEY=YOUR_API_KEY
     ```

## Usage

1. Run the application:

   ```bash
   python app.py
   ```

2. The application will start a conversation loop where you can enter your requests or queries.

3. Enter your request or query and press Enter. The application will process your request, generate a response, and display it along with sub-questions related to your query.

4. Continue the conversation by entering more requests or queries.

5. To exit the application, enter one of the following commands: "bye", "goodbye", "exit", or "quit".

## Customization

- You can customize the project data by modifying the `sample_data` dictionary in the code. Update the project details, tasks, resources, and other relevant information according to your specific project.

- The `custom_functions` list defines the available functions that can be called by the OpenAI model. You can add or modify the functions based on your requirements.

- The `process_user_request` function handles the user's request and generates a response using the OpenAI model. You can customize this function to include additional logic or functionality.

## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvement, please open an issue or submit a pull request.

## License

This project is licensed under the [MIT License](LICENSE).

## Acknowledgments

- [OpenAI](https://www.openai.com/) for providing the language model and function calling capabilities.
- [Llama Index](https://github.com/jerryjliu/llama_index) for the OpenAI Question Generator.
