from connectors.hcp import get_hcp_documents
from connectors.mef import get_mef_documents
from connectors.imf import get_imf_documents
from connectors.worldbank import (
    get_worldbank_documents
)
from connectors.oecd import (
    get_oecd_documents
)
from connectors.bam import (
    get_bam_documents
)


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

        print(
            f"{name}: {len(docs)} documents"
        )

        return [
            normalize(x)
            for x in docs
        ]

    except Exception as e:

        print(
            f"{name} ERROR: {e}"
        )

        return []


def get_all_documents():

    documents = []

    sources = [
        ("HCP", get_hcp_documents),
        ("MEF", get_mef_documents),
        ("IMF", get_imf_documents),
        ("WORLDBANK", get_worldbank_documents),
        ("OCDE", get_oecd_documents),
        ("BAM", get_bam_documents),
    ]

    for name, source in sources:

        documents.extend(
            load_source(
                name,
                source
            )
        )

    print(
        f"TOTAL: {len(documents)} documents"
    )

    return documents
