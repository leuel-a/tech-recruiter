import os
import requests

API_BASE_URL = "https://api.github.com"
GITHUB_ACCESS_TOKEN = os.getenv('GITHUB_API_TOKEN', '')


async def search_candidates():
    headers = {
            "Accept": "application/vnd.github+json",
            "X-Github-Api-Version": "2022-11-28",
            "Authorization": f"Bearer {GITHUB_ACCESS_TOKEN}"
        }

    response = requests.get(API_BASE_URL + "/users", headers=headers)
    return response

