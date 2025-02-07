from medclimate.api import app
from fastapi.testclient import TestClient

MedAPI = TestClient(app)



def test_read_main():
    """Test the root endpoint"""
    response = MedAPI.get("/")


    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to MedClimate API"}


def test_health_check():
    """Test the health check endpoint"""
    response=MedAPI.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}
