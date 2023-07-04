from fastapi.testclient import TestClient
from main import app



client = TestClient(app=app)

def test_get_or_jobs():
    response = client.get("/jobs")
    assert response.status_code == 500

def test_search_jobs():
    response = client.get("/search_jobs")
    assert response.status_code == 422

def test_create_profile():
    
    new_profile_data = {
        "first_name": "John",
        "last_name": "Doe",
        "email_address": "john.doe@example.com",
        "city": "New York",
        "phone_number": "123456789",
        "job_prefernece_title": "Software Developer",
        "job_prefernece_type": "Full-time"
    }

    
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJuZW8iLCJleHAiOjE2ODgxNDM5NzR9.RQIun7GyEwWLE4rAMiwL4qEiaZaO3pKlYSFqQtR7o_w"

    
    headers = {
        "Authorization": f"Bearer {token}"
    }

    
    response = client.post("/create_profile", json=new_profile_data, headers=headers)

    
    assert response.status_code == 200

    
    assert response.json() == {
        "user": "<username>",
        "first_name": "John",
        "last_name": "Doe",
        "email_address": "john.doe@example.com",
        "city": "New York",
        "phone_number": "123456789",
        "job_prefernece_title": "Software Developer",
        "job_prefernece_type": "Full-time"
    }

print(r)



    

