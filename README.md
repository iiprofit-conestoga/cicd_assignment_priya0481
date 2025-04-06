# Azure Function CI/CD Pipeline Project

This project demonstrates a CI/CD pipeline using Jenkins to deploy a Python Azure Function to Azure Functions.

## Project Structure
- `function_app.py`: Main Azure Function implementation
- `test_function.py`: Test cases for the Azure Function
- `requirements.txt`: Python dependencies
- `Jenkinsfile`: Jenkins pipeline configuration
- `function.json`: Azure Function configuration
- `host.json`: Azure Functions host configuration
- `local.settings.json`: Local development settings

## Prerequisites
- Python 3.12 or higher
- Azure CLI
- Jenkins server with configured credentials:
  - Azure Service Principal credentials
  - GitHub Personal Access Token
- Azure Function App created in Azure Portal

## Local Development
1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: .\venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run tests locally:
   ```bash
   python -m pytest test_function.py -v
   ```

## CI/CD Pipeline
The Jenkins pipeline consists of three stages:
1. Build: Sets up Python environment and installs dependencies
2. Test: Runs automated tests
3. Deploy: Deploys the function to Azure Functions

The pipeline is triggered automatically when changes are pushed to the main branch.

## Test Cases
The project includes three test cases:
1. Verifies the response contains "Hello, World!"
2. Checks if the status code is 200
3. Validates the response type is correct

## Deployment
The function is automatically deployed to Azure Functions when changes are pushed to the main branch.
The deployed function returns "Hello, World!" along with the current timestamp.

## Author
Kirtirajsinh Solanki
