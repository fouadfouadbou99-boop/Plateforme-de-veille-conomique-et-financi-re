"""
Agrégateur central des actualités.
"""

try:
    from connectors.bam import get_bam_documents
except Exception:
    def get_bam_documents():
        return []


try:
    from connectors.imf import get_imf_documents
except Exception:
    def get_imf_documents():
        return []


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


def normalize(item):

    if not isinstance(item, dict):
        return None

    return {
        "Source": item.get("Source", ""),
        "Titre": item.get("Titre", ""),
        "Date": item.get("Date", ""),
        "Lien": item.get("Lien", ""),
        "PDF": item.get("PDF", ""),
    }


def get_all_documents():

    documents = []

    sources = [
        get_bam_documents,
        get_imf_documents,
        get_hcp_documents,
        get_mef_documents,
    ]

    for source in sources:

        try:

            result = source()

            if result:

                for item in result:

                    item = normalize(item)

                    if item:
                        documents.append(item)

        except Exception as e:

            print(
                f"Erreur source {source.__name__}: {e}"
            )

    return documents
