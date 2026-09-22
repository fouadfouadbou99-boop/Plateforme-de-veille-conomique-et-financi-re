"""
connectors/aggregator.py
"""

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


try:
    from connectors.worldbank import get_worldbank_documents
except Exception:
    def get_worldbank_documents():
        return []


def normalize_record(item):

    if not isinstance(item, dict):
        return None

    return {
        "Source": item.get("Source", ""),
        "Titre": item.get("Titre", ""),
        "Date": item.get("Date", ""),
        "Lien": item.get("Lien", ""),
        "PDF": item.get("PDF", ""),
    }


def process_source(source_name, source_function):

    try:

        data = source_function()

        if not data:
            print(f"{source_name}: 0 document")
            return []

        results = []

        for item in data:

            normalized = normalize_record(item)

            if normalized:
                results.append(normalized)

        print(
            f"{source_name}: {len(results)} documents"
        )

        return results

    except Exception as e:

        print(
            f"{source_name} ERROR: {e}"
        )

        return []


def get_all_documents():

    documents = []

    documents.extend(
        process_source(
            "HCP",
            get_hcp_documents
        )
    )

    documents.extend(
        process_source(
            "MEF",
            get_mef_documents
        )
    )

    documents.extend(
        process_source(
            "IMF",
            get_imf_documents
        )
    )

    documents.extend(
        process_source(
            "BAM",
            get_bam_documents
        )
    )

    documents.extend(
        process_source(
            "WorldBank",
            get_worldbank_documents
        )
    )

    documents.sort(
        key=lambda x: str(x["Date"]),
        reverse=True
    )

    print(
        f"TOTAL: {len(documents)} documents"
    )

    return documents
