import pytest
from unittest.mock import patch, MagicMock
from src.api_client import fetch_random_users

@patch('requests.get')
def test_fetch_random_users_success(mock_get):
    # Mock response
    mock_resp = MagicMock()
    mock_resp.status_code = 200
    mock_resp.json.return_value = {"results": [{"name": "fake"}]}
    mock_get.return_value = mock_resp
    
    result = fetch_random_users(results=1)
    
    assert "results" in result
    assert len(result["results"]) == 1
    mock_get.assert_called_once()

@patch('requests.get')
def test_fetch_random_users_fallback(mock_get):
    mock_resp = MagicMock()
    mock_resp.status_code = 500
    mock_resp.raise_for_status.side_effect = Exception("API Error")
    mock_get.return_value = mock_resp
    
    # Should not raise, should return mock data
    result = fetch_random_users()
    assert "results" in result
    assert len(result["results"]) > 0
    assert result["results"][0]["name"]["first"] == "Alice"
