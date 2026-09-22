import requests

URL = "https://www.bkam.ma/Communiques"


def get_bam_documents():

    try:

        response = requests.get(
            URL,
            timeout=60,
            headers={
                "User-Agent": (
                    "Mozilla/5.0 "
                    "(Windows NT 10.0; Win64; x64)"
                )
            }
        )

        if response.status_code != 200:

            print(
                f"BAM ERROR HTTP {response.status_code}"
            )

            return []

        return [
            {
                "Source": "BAM",
                "Titre": "Communiqués BAM",
                "Date": "",
                "Lien": URL,
                "PDF": ""
            }
        ]

    except Exception as e:

        print(f"BAM ERROR: {e}")

        return []
