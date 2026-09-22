from connectors.hcp import get_hcp_documents
from connectors.mef import get_mef_documents
from connectors.imf import get_imf_documents
from connectors.worldbank import get_worldbank_documents
from connectors.oecd import get_oecd_documents
from connectors.bam import get_bam_documents


def normalize(doc):

    return {
        "Source": doc.get("Source", ""),
        "Titre": doc.get("Titre", ""),
        "Date": doc.get("Date", ""),
        "Lien": doc.get("Lien", ""),
        "PDF": doc.get("PDF", "")
    }


def get_all_documents():

    documents = []

    sources = [
        get_hcp_documents,
        get_mef_documents,
        get_imf_documents,
        get_worldbank_documents,
        get_oecd_documents,
        get_bam_documents,
    ]

    for source in sources:

        try:

            data = source()

            if data:

                documents.extend(
                    [
                        normalize(x)
                        for x in data
                    ]
                )

        except Exception as e:

            print(
                f"{source.__name__}: {e}"
            )

    return documents
