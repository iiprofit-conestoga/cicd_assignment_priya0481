pipeline {
    agent any
    
    triggers {
        // GitHub webhook trigger
        githubPush()
    }
    
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
                        python3 --version
                        python3 -m venv venv
                        . venv/bin/activate
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
                        . venv/bin/activate
                        python -m pytest test_function.py -v
                    '''
                }
            }
        }
        
        stage('Package') {
            steps {
                script {
                    echo 'Creating deployment package...'
                    sh '''
                        # Create deployment directory
                        mkdir -p deploy/HttpTrigger
                        
                        # Copy function code
                        cp function_app.py deploy/HttpTrigger/__init__.py
                        
                        # Copy configuration files
                        cp requirements.txt deploy/
                        cp host.json deploy/
                        cp local.settings.json deploy/
                        
                        # Create function.json for the HTTP trigger
                        cat > deploy/HttpTrigger/function.json << 'EOF'
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
EOF
                        
                        # Create deployment package
                        zip -r function_package.zip deploy/*
                        
                        # Verify package contents
                        mkdir -p verify_package
                        unzip -l function_package.zip
                    '''
                }
            }
        }
        
        stage('Deploy to Azure') {
            steps {
                script {
                    echo 'Deploying to Azure...'
                    sh '''
                        # Login to Azure
                        az login --service-principal -u $AZURE_CLIENT_ID -p $AZURE_CLIENT_SECRET --tenant $AZURE_TENANT_ID
                        az account set --subscription $AZURE_SUBSCRIPTION_ID
                        
                        # Create function app if it doesn't exist
                        if ! az functionapp show --name $FUNCTION_APP_NAME --resource-group $RESOURCE_GROUP &> /dev/null; then
                            echo "Creating new function app..."
                            az functionapp create \
                                --name $FUNCTION_APP_NAME \
                                --resource-group $RESOURCE_GROUP \
                                --storage-account $STORAGE_ACCOUNT \
                                --runtime python \
                                --runtime-version $PYTHON_VERSION \
                                --functions-version $FUNCTIONS_VERSION \
                                --os-type linux \
                                --consumption-plan-location $LOCATION \
                                --https-only true
                            
                            # Configure Python settings
                            echo "Configuring Python settings..."
                            az functionapp config appsettings set \
                                --name $FUNCTION_APP_NAME \
                                --resource-group $RESOURCE_GROUP \
                                --settings \
                                PYTHON_ENABLE_WORKER_EXTENSIONS=1 \
                                PYTHON_ISOLATION_LEVEL=ISOLATED
                        else
                            echo "Function app already exists."
                        fi
                        
                        # Deploy the function
                        echo "Deploying function package..."
                        az functionapp deployment source config-zip \
                            --name $FUNCTION_APP_NAME \
                            --resource-group $RESOURCE_GROUP \
                            --src function_package.zip
                        
                        # Wait for function app to be ready
                        echo "Waiting for function app to be ready..."
                        sleep 30
                        
                        # List functions to verify deployment
                        echo "Listing functions..."
                        az functionapp function list \
                            --name $FUNCTION_APP_NAME \
                            --resource-group $RESOURCE_GROUP
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