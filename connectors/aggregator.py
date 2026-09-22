from connectors.hcp import get_hcp_documents
from connectors.mef import get_mef_documents

try:
    from connectors.imf import get_imf_documents
except Exception:
    def get_imf_documents():
        return []


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

        docs = func()

        print(f"{name}: {len(docs)} documents")

        return [
            normalize(x)
            for x in docs
        ]

    except Exception as e:

        print(f"{name} ERROR: {e}")

        return []


def get_all_documents():

    documents = []

    documents.extend(
        load_source(
            "HCP",
            get_hcp_documents
        )
    )

    documents.extend(
        load_source(
            "MEF",
            get_mef_documents
        )
    )

    documents.extend(
        load_source(
            "IMF",
            get_imf_documents
        )
    )

    print(
        f"TOTAL: {len(documents)} documents"
    )

    return documents
