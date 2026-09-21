"""
Agrégation centralisée des documents provenant
des différentes sources de veille.
"""

from connectors.bam import get_bam_documents
from connectors.imf import get_imf_documents

try:
    from connectors.hcp import get_hcp_documents
except Exception:
    def get_hcp_documents():
        return []

try:
    from connectors.mef import get_mef_documents
except Exception:
    def get_mef_documents():
        return []


def normalize(record):
    """
    Garantit la présence des colonnes attendues
    par Streamlit.
    """

    if not isinstance(record, dict):
        return None

    return {
        "Source": record.get("Source", ""),
        "Titre": record.get("Titre", ""),
        "Date": record.get("Date", ""),
        "Lien": record.get("Lien", ""),
        "PDF": record.get("PDF", ""),
    }


def load_source(source_function, source_name):
    """
    Charge une source sans bloquer toute l'application
    en cas d'erreur.
    """

    try:
        data = source_function()

        if not data:
            return []

        records = []

        for item in data:
            item = normalize(item)

            if item:
                records.append(item)

        print(f"{source_name}: {len(records)} documents")

        return records

    except Exception as exc:

        print(
            f"Erreur source {source_name}: {exc}"
        )

        return []


def get_all_documents():
    """
    Fonction principale appelée par
    pages/1_Actualites.py
    """

    documents = []

    documents.extend(
        load_source(
            get_bam_documents,
            "BAM"
        )
    )

    documents.extend(
        load_source(
            get_hcp_documents,
            "HCP"
        )
    )

    documents.extend(
        load_source(
            get_mef_documents,
            "MEF"
        )
    )

    documents.extend(
        load_source(
            get_imf_documents,
            "IMF"
        )
    )

    documents.sort(
        key=lambda x: str(x.get("Date", "")),
        reverse=True
    )

    return documents
``
