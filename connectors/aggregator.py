from connectors.hcp import get_hcp_documents
from connectors.mef import get_mef_documents
from connectors.bam import get_bam_documents
from connectors.worldbank import get_worldbank_documents

try:
    from connectors.imf import get_imf_documents
except:
    def get_imf_documents():
        return []

try:
    from connectors.oecd import get_oecd_documents
except:
    def get_oecd_documents():
        return []

try:
    from connectors.ecb import get_ecb_documents
except:
    def get_ecb_documents():
        return []

try:
    from connectors.bdf import get_bdf_documents
except:
    def get_bdf_documents():
        return []


def get_all_documents():

    documents = []

    sources = [

        ("HCP", get_hcp_documents),

        ("MEF", get_mef_documents),

        ("BAM", get_bam_documents),

        ("Banque Mondiale", get_worldbank_documents),

        ("FMI", get_imf_documents),

        ("OCDE", get_oecd_documents),

        ("BCE", get_ecb_documents),

        ("Banque de France", get_bdf_documents)

    ]

    for name, source in sources:

        try:

            docs = source()

            if docs:

                print(
                    f"{name}: {len(docs)} documents"
                )

                documents.extend(
                    docs
                )

            else:

                print(
                    f"{name}: 0 document"
                )

        except Exception as e:

            print(
                f"{name} ERROR: {e}"
            )

    return documents
