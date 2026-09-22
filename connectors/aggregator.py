from connectors.hcp import get_hcp_documents
from connectors.mef import get_mef_documents
from connectors.imf import get_imf_documents


def normalize(doc):

    return {
        "Source": doc.get("Source", ""),
        "Titre": doc.get("Titre", ""),
        "Date": doc.get("Date", ""),
        "Lien": doc.get("Lien", ""),
        "PDF": doc.get("PDF", "")
    }


def load_source(name, func):

    try:

        data = func()

        print(f"{name}: {len(data)} documents")

        return [normalize(x) for x in data]

    except Exception as e:

        print(f"{name} ERROR: {e}")

        return []


def get_all_documents():

    docs = []

    docs.extend(
        load_source(
            "HCP",
            get_hcp_documents
        )
    )

    docs.extend(
        load_source(
            "MEF",
            get_mef_documents
        )
    )

    docs.extend(
        load_source(
            "IMF",
            get_imf_documents
        )
    )

    return docs
