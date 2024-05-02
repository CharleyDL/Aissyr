import requests
import os


DAGSHUB_REPO = os.getenv('DAGSHUB_REPO')
DAGSHUB_REPO_OWNER = os.getenv('DAGSHUB_REPO_OWNER')
MODEL_URI = os.getenv('MODEL_URI')
DAGSHUB_USER_TOKEN = os.getenv('DAGSHUB_USER_TOKEN')


token = 'a4069f9e2a4a499a4a760c37d7890d1d775d651b'
# url = "https://dagshub.com/api/v1/user"
# headers = {"Authorization": f"Bearer {token}"}

# print(requests.get(url, headers=headers).json())


url = f"https://dagshub.com/api/v1/repos/{DAGSHUB_REPO_OWNER}/{DAGSHUB_REPO}"
headers = {"Authorization": f"Bearer {token}"}

print(requests.get(url, headers=headers).json())