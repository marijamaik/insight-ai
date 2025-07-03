# Backend API communication
import requests
from dotenv import load_dotenv
import os

load_dotenv()
api_url = os.getenv("API_BASE_URL")

class InsightAIClient:
    def __init__(self, base_url=api_url):
        self.base_url = base_url

    def health_check(self):
        try:
            response = requests.get(f"{self.base_url}/")
            return response.status_code == 200
        except:
            return False

    def upload_file(self, file):
        try:
            files = {'file': (file.name, file.getvalue(), file.type)}
            response = requests.post(f"{self.base_url}/data/upload", files=files)
            return response.status_code == 200, response.json()
        except Exception as e:
            return False, {"error": str(e)}

    def list_datasets(self):
        try:
            response = requests.get(f"{self.base_url}/datasets")
            return response.status_code == 200, response.json()
        except Exception as e:
            return False, {"error": str(e)}

    def get_dataset(self, dataset_id):
        try:
            response = requests.get(f"{self.base_url}/datasets/{dataset_id}")
            return response.status_code == 200, response.json()
        except Exception as e:
            return False, {"error": str(e)}

    def delete_dataset(self, dataset_id):
        try:
            response = requests.delete(f"{self.base_url}/datasets/{dataset_id}")
            return response.status_code == 200, response.json()
        except Exception as e:
            return False, {"error": str(e)}
