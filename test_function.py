import pytest
from HttpTrigger.function_app import main
import azure.functions as func
import json
from datetime import datetime

@pytest.mark.asyncio
async def test_function_http_trigger():
    # Create a mock HTTP request
    req = func.HttpRequest(
        method='GET',
        url='/api/hello',
        body=None,
        params={}
    )
    
    # Call the function
    response = main(req)
    
    # Assert response status code is 200
    assert response.status_code == 200
    
    # Get response body
    response_body = response.get_body().decode()
    
    # Assert response contains "Hello, World!"
    assert "Hello, World!" in response_body
    
    # Assert response contains a timestamp
    assert "Current time:" in response_body

@pytest.mark.asyncio
async def test_status_code():
    # Test case 2: Check if status code is 200
    req = func.HttpRequest(
        method='GET',
        url='/api/hello',
        body=None
    )
    response = main(req)
    assert response.status_code == 200

@pytest.mark.asyncio
async def test_response_type():
    # Test case 3: Check if response is of correct type
    req = func.HttpRequest(
        method='GET',
        url='/api/hello',
        body=None
    )
    response = main(req)
    assert isinstance(response, func.HttpResponse) 