import requests

def get_latest_data():

    url = "https://sdmx.oecd.org/public/rest/dataflow"

    response = requests.get(
        url,
        timeout=30
    )

    return response.json()
