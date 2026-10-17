import pytest
from fastapi.testclient import TestClient

# Simple test that avoids the bcrypt import-time issues by mocking at module level
import sys
from unittest.mock import patch

# Mock bcrypt at the system level before importing anything that uses it
with patch('passlib.context.CryptContext.hash') as mock_hash, \
     patch('passlib.context.CryptContext.verify') as mock_verify:
    mock_hash.return_value = "$2b$12$abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0"
    mock_verify.return_value = True

    # Now import the app
    from api.main import app

client = TestClient(app)

def test_health_check():
    """Test the health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_root_endpoint():
    """Test the root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Control API is running"}