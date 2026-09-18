import requests

BASE_URL = "https://dataservices.imf.org/REST"

def get_datasets():

    response = requests.get(
        BASE_URL,
        timeout=30
    )

    return response.json()
