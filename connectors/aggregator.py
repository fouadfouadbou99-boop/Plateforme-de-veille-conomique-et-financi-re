from connectors.bam import get_bam_documents
from connectors.imf import get_imf_documents


def normalize(record):

    if not isinstance(record, dict):
        return None

    return {
        "Source": record.get("Source", ""),
        "Titre": record.get("Titre", ""),
        "Date": record.get("Date", ""),
        "Lien": record.get("Lien", ""),
        "PDF": record.get("PDF", ""),
    }


def get_all_documents():

    documents = []

    try:
        documents.extend(
            [
                normalize(x)
                for x in get_bam_documents()
            ]
        )
    except Exception as e:
        print(f"BAM : {e}")

    try:
        documents.extend(
            [
                normalize(x)
                for x in get_imf_documents()
            ]
        )
    except Exception as e:
        print(f"IMF : {e}")

    documents = [
        doc
        for doc in documents
        if doc is not None
    ]

    return documents
