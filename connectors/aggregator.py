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


def load_source(name, loader):

    try:

        docs = loader()

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

    docs.extend(
        load_source(
            "WORLDBANK",
            get_worldbank_documents
        )
    )

    docs.extend(
        load_source(
            "OCDE",
            get_oecd_documents
        )
    )

    docs.extend(
        load_source(
            "BAM",
            get_bam_documents
        )
    )

    print(
        f"TOTAL: {len(docs)} documents"
    )

    return docs
