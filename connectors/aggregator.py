try:
    from connectors.bam import get_bam_documents
except Exception:
    def get_bam_documents():
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

try:
    from connectors.imf import get_imf_documents
except Exception:
    def get_imf_documents():
        return []


def get_all_documents():

    docs = []

    docs.extend(get_bam_documents())
    docs.extend(get_hcp_documents())
    docs.extend(get_mef_documents())
    docs.extend(get_imf_documents())

    return docs
