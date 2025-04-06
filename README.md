# Azure Function App with CI/CD Pipeline

This project demonstrates a CI/CD pipeline for deploying an Azure Function App using Jenkins and GitHub.

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
- Jenkins server
- GitHub account
- Azure subscription with service principal having Contributor access to the resource group

## Local Development
1. Clone the repository
2. Create a virtual environment: `python -m venv venv`
3. Activate the virtual environment:
   - Windows: `venv\Scripts\activate`
   - Linux/Mac: `source venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Run tests: `python -m pytest`

## CI/CD Pipeline
The pipeline consists of the following stages:
1. Checkout: Clones the repository
2. Build: Sets up Python environment and installs dependencies
3. Test: Runs unit tests
4. Package: Creates deployment package
5. Deploy: Deploys to Azure Function App

The pipeline is triggered automatically when changes are pushed to the main branch. It uses GitHub webhooks and periodic polling (every 5 minutes) to detect changes.

## Test Cases
The project includes test cases for the Azure Function:
- Test successful HTTP trigger
- Test error handling
- Test response format

## Deployment
The application is deployed to Azure Function App using Azure CLI. The deployment process:
1. Creates a deployment package
2. Authenticates with Azure using service principal
3. Deploys the package to the Function App

The function app is deployed to: https://priya-function.azurewebsites.net/api/hello

## Author
Priya Patel (Student ID: 8860481)
