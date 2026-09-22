from connectors.hcp import get_hcp_documents
from connectors.mef import get_mef_documents
from connectors.imf import get_imf_documents

try:
    from connectors.bam import get_bam_documents
except Exception:
    def get_bam_documents():
        return []

try:
    from connectors.worldbank import get_worldbank_documents
except Exception:
    def get_worldbank_documents():
        return []


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
        ("HCP", get_hcp_documents),
        ("MEF", get_mef_documents),
        ("IMF", get_imf_documents),
        ("BAM", get_bam_documents),
        ("WORLDBANK", get_worldbank_documents),
    ]

    for source_name, source_function in sources:

        try:

            data = source_function()

            if data:

                documents.extend(
                    [
                        normalize(x)
                        for x in data
                    ]
                )

            print(
                f"{source_name}: {len(data)} documents"
            )

        except Exception as e:

            print(
                f"{source_name} ERROR: {e}"
            )

    return documents
