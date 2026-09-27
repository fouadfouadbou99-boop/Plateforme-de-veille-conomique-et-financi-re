from connectors.hcp import get_hcp_documents
from connectors.mef import get_mef_documents

# BAM
try:
    from connectors.bam import get_bam_documents
except Exception:
    def get_bam_documents():
        return []

# FMI
try:
    from connectors.imf import get_imf_documents
except Exception:
    def get_imf_documents():
        return []

# OCDE
try:
    from connectors.oecd import get_oecd_documents
except Exception:
    def get_oecd_documents():
        return []

# Banque mondiale
try:
    from connectors.worldbank import (
        get_worldbank_documents
    )
except Exception:
    def get_worldbank_documents():
        return []


def get_all_documents():

    documents = []

    sources = [

        ("HCP", get_hcp_documents),

        ("MEF", get_mef_documents),

        ("BAM", get_bam_documents),

        ("FMI", get_imf_documents),

        ("OCDE", get_oecd_documents),

        (
            "Banque Mondiale",
            get_worldbank_documents
        )

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
