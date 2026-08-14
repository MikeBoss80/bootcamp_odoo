import requests


EXTERNAL_API_URL = "http://external-api:8000"


def get_publishers():
    response = requests.get(
        f"{EXTERNAL_API_URL}/publishers"
    )

    response.raise_for_status()

    return response.json()