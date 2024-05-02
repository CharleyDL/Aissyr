import os
import sys

from fastapi.testclient import TestClient
from dotenv import load_dotenv

## Add the current directory to the path
sys.path.append(".")
from api import app


load_dotenv()


class TestArchiveClassification:

    client = TestClient(app)
    API_URL = os.getenv("API_URL")

    def test_archive_classification_found(self):
        response = self.client.get(url=f"{self.API_URL}/archives/classification/")

        assert response.status_code == 200
        assert response.json()["result"] == True
        assert response.json()["message"] == "Archive classification found"
        assert response.json()["content"] is not None


class TestArchiveLabelisation:

    client = TestClient(app)
    API_URL = os.getenv("API_URL")

    def test_archive_labelisation_found(self):
        response = self.client.get(url=f"{self.API_URL}/archives/labelisation/")

        assert response.status_code == 200
        assert response.json()["result"] == True
        assert response.json()["message"] == "Archive labelisation found"
        assert response.json()["content"] is not None
