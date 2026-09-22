from connectors.hcp import get_hcp_documents
from connectors.mef import get_mef_documents

try:
    from connectors.imf import get_imf_documents
except Exception:
    def get_imf_documents():
        return []

try:
    from connectors.bam import get_bam_documents
except Exception:
    def get_bam_documents():
        return []


def get_all_documents():

    documents = []

    sources = [
        ("HCP", get_hcp_documents),
        ("MEF", get_mef_documents),
        ("IMF", get_imf_documents),
        ("BAM", get_bam_documents),
    ]

    for name, source in sources:

        try:

            docs = source()

            print(
                f"{name}: {len(docs)} documents"
            )

            documents.extend(docs)

        except Exception as e:

            print(
                f"{name} ERROR: {e}"
            )

    return documents
