import os
import pytest
import sys

from fastapi.testclient import TestClient
from dotenv import load_dotenv

## Add the current directory to the path
sys.path.append(".")
from api import app


load_dotenv()


class TestAPIAccount:

    client = TestClient(app)
    API_URL = os.getenv("API_URL")

    @pytest.mark.parametrize("email, input_pwd, expected_result", [
        ("DEMO", "demotest", True),
        ("wrong@example.com", "badpass", False)
    ])
    def test_verify_login(self, email, input_pwd, expected_result):
        credentials = {
            "email": email,
            "input_pwd": input_pwd
        }

        response = self.client.post(
            url=f"{self.API_URL}/account/verify_login/",
            json=credentials
        )

        assert response.status_code == 200 
        assert response.json()["result"] == expected_result
