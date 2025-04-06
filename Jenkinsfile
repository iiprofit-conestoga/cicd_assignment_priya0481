pipeline {
    agent any
    
    environment {
        // Azure credentials and configuration for assignment.
        AZURE_SUBSCRIPTION_ID = credentials('AZURE_SUBSCRIPTION_ID')
        AZURE_TENANT_ID = credentials('AZURE_TENANT_ID')
        AZURE_CLIENT_ID = credentials('AZURE_CLIENT_ID')
        AZURE_CLIENT_SECRET = credentials('AZURE_CLIENT_SECRET')
        FUNCTION_APP_NAME = 'priya-function'
        RESOURCE_GROUP = 'priya-rg'
        STORAGE_ACCOUNT = 'priyastorageacc123'
        PYTHON_VERSION = '3.12'
        FUNCTIONS_VERSION = '4'
        LOCATION = 'eastus'
    }

    stages {
        stage('Checkout') {
            steps {
                echo 'Checking out the code from Git'
                checkout scm
            }
        }
        
        stage('Build') {
            steps {
                script {
                    echo 'Setting up Python environment...'
                    sh '''
                        python --version
                        python -m venv venv
                        . venv/Scripts/activate
                        python -m pip install --upgrade pip
                        python -m pip install --no-cache-dir -r requirements.txt
                    '''
                }
            }
        }
        
        stage('Test') {
            steps {
                script {
                    echo 'Running tests...'
                    sh '''
                        . venv/Scripts/activate
                        python -m pytest test_function.py -v
                    '''
                }
            }
        }
        
        stage('Package') {
            steps {
                script {
                    echo 'Creating deployment package...'
                    powershell '''
                        # Create deployment directory
                        New-Item -ItemType Directory -Force -Path deploy
                        
                        # Create function directory structure
                        New-Item -ItemType Directory -Force -Path deploy/HttpTrigger
                        
                        # Copy function code
                        Copy-Item -Path function_app.py -Destination deploy/HttpTrigger/__init__.py
                        
                        # Copy configuration files
                        Copy-Item -Path requirements.txt -Destination deploy/
                        Copy-Item -Path host.json -Destination deploy/
                        Copy-Item -Path local.settings.json -Destination deploy/
                        
                        # Create function.json for the HTTP trigger
                        $functionJson = @"
{
  "scriptFile": "__init__.py",
  "bindings": [
    {
      "authLevel": "anonymous",
      "type": "httpTrigger",
      "direction": "in",
      "name": "req",
      "methods": [
        "get",
        "post",
        "options"
      ],
      "route": "hello"
    },
    {
      "type": "http",
      "direction": "out",
      "name": "$return"
    }
  ]
}
"@
                        Set-Content -Path deploy/HttpTrigger/function.json -Value $functionJson
                        
                        # Create deployment package
                        Compress-Archive -Path deploy/* -DestinationPath function_package.zip -Force
                        
                        # Verify package contents
                        New-Item -ItemType Directory -Force -Path verify_package
                        Expand-Archive -Path function_package.zip -DestinationPath verify_package
                        Get-ChildItem -Path verify_package -Recurse
                    '''
                }
            }
        }
        
        stage('Deploy to Azure') {
            steps {
                script {
                    echo 'Deploying to Azure...'
                    powershell '''
                        # Login to Azure
                        az login --service-principal -u $env:AZURE_CLIENT_ID -p $env:AZURE_CLIENT_SECRET --tenant $env:AZURE_TENANT_ID
                        az account set --subscription $env:AZURE_SUBSCRIPTION_ID
                        
                        # Create function app if it doesn't exist
                        $functionApp = az functionapp show --name $env:FUNCTION_APP_NAME --resource-group $env:RESOURCE_GROUP 2>$null
                        if (-not $functionApp) {
                            Write-Host "Creating new function app..."
                            az functionapp create `
                                --name $env:FUNCTION_APP_NAME `
                                --resource-group $env:RESOURCE_GROUP `
                                --storage-account $env:STORAGE_ACCOUNT `
                                --runtime python `
                                --runtime-version $env:PYTHON_VERSION `
                                --functions-version $env:FUNCTIONS_VERSION `
                                --os-type linux `
                                --consumption-plan-location $env:LOCATION `
                                --https-only true
                            
                            # Configure Python settings
                            Write-Host "Configuring Python settings..."
                            az functionapp config appsettings set `
                                --name $env:FUNCTION_APP_NAME `
                                --resource-group $env:RESOURCE_GROUP `
                                --settings `
                                PYTHON_ENABLE_WORKER_EXTENSIONS=1 `
                                PYTHON_ISOLATION_LEVEL=ISOLATED
                        } else {
                            Write-Host "Function app already exists."
                        }
                        
                        # Deploy the function
                        Write-Host "Deploying function package..."
                        az functionapp deployment source config-zip `
                            --name $env:FUNCTION_APP_NAME `
                            --resource-group $env:RESOURCE_GROUP `
                            --src function_package.zip
                        
                        # Wait for function app to be ready
                        Write-Host "Waiting for function app to be ready..."
                        Start-Sleep -Seconds 30
                        
                        # List functions to verify deployment
                        Write-Host "Listing functions..."
                        az functionapp function list `
                            --name $env:FUNCTION_APP_NAME `
                            --resource-group $env:RESOURCE_GROUP
                    '''
                }
            }
        }
    }

    post {
        always {
            cleanWs()
            echo 'Cleaning up workspace...'
        }
        success {
            script {
                echo '''
===========================================
Pipeline completed successfully!
===========================================
Function App Details:
-------------------
Name: priya-function
Resource Group: priya-rg
Location: East US

Function URLs:
-------------
Main Function URL: https://priya-function.azurewebsites.net/api/hello
SCM URL: https://priya-function.scm.azurewebsites.net

You can test the function using:
1. Browser: https://priya-function.azurewebsites.net/api/hello
2. cURL: curl https://priya-function.azurewebsites.net/api/hello
3. Postman: GET https://priya-function.azurewebsites.net/api/hello

Note: The function may take a few minutes to be fully available after deployment.
===========================================
'''
            }
        }
        failure {
            echo 'Pipeline failed!'
        }
    }
} 