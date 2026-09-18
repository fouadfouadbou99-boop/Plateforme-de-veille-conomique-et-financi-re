import requests

BASE_URL = "https://api.worldbank.org/v2"

def get_indicators():

    endpoint = f"{BASE_URL}/indicator"

    params = {
        "format": "json",
        "per_page": 100
    }

    response = requests.get(
        endpoint,
        params=params,
        timeout=30
    )

    return response.json()
