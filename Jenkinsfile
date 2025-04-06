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
        FUNCTION_APP = 'priya-function'
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
                        mkdir -p deploy/HttpTrigger
                        cp HttpTrigger/function_app.py deploy/HttpTrigger/__init__.py
                        cp HttpTrigger/function.json deploy/HttpTrigger/
                        cp host.json deploy/
                        cp requirements.txt deploy/
                        cd deploy
                        zip -r ../function.zip .
                    '''
                }
            }
        }
        
        stage('Deploy to Azure') {
            steps {
                script {
                    echo 'Deploying to Azure Function App...'
                    withCredentials([usernamePassword(credentialsId: 'azure-credentials', usernameVariable: 'AZURE_CLIENT_ID', passwordVariable: 'AZURE_CLIENT_SECRET')]) {
                        sh '''
                            az login --service-principal -u $AZURE_CLIENT_ID -p $AZURE_CLIENT_SECRET --tenant $AZURE_TENANT_ID
                            az account set --subscription $AZURE_SUBSCRIPTION_ID
                            az functionapp deployment source config-zip -g $RESOURCE_GROUP -n $FUNCTION_APP --src function.zip
                        '''
                    }
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