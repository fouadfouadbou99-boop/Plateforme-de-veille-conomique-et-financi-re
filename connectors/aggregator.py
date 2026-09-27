from connectors.hcp import get_hcp_documents
from connectors.mef import get_mef_documents
from connectors.bam import get_bam_documents
from connectors.worldbank import get_worldbank_documents
from connectors.ecb import get_ecb_documents

try:
    from connectors.imf import get_imf_documents
except Exception:
    def get_imf_documents():
        return []

try:
    from connectors.oecd import get_oecd_documents
except Exception:
    def get_oecd_documents():
        return []


def get_all_documents():

    documents = []

    sources = [

        ("HCP", get_hcp_documents),

        ("MEF", get_mef_documents),

        ("BAM", get_bam_documents),

        ("Banque Mondiale",
         get_worldbank_documents),

        ("BCE",
         get_ecb_documents),

        ("FMI",
         get_imf_documents),

        ("OCDE",
         get_oecd_documents)

    ]

    for name, source in sources:

        try:

            docs = source()

            print(
                f"{name}: {len(docs)} documents"
            )

            if docs:
                documents.extend(docs)

        except Exception as e:

            print(
                f"{name} ERROR: {e}"
            )

    return documents
