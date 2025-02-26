import pytest
from modular_api.api_client import APIClient
from requests.exceptions import HTTPError

# Create a test instance of APIClient (default: retries enabled)
api_client = APIClient("https://jsonplaceholder.typicode.com")


def test_get_request():
    """Test GET request to a valid endpoint."""
    response = api_client.request("/posts/1")
    assert isinstance(response, dict)  # Response should be a dictionary
    assert "id" in response  # Response should contain an 'id' field
    assert response["id"] == 1  # The ID should match the request


def test_invalid_endpoint():
    """Test GET request to an invalid endpoint, expecting a 404 error without retries."""

    api_client_no_retry = APIClient("https://jsonplaceholder.typicode.com", retries=False)  # ✅ Disable retries

    with pytest.raises(HTTPError) as excinfo:
        api_client_no_retry.request("/invalid_endpoint")  # Call the method

    assert "404 Client Error" in str(excinfo.value)
