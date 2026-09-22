from connectors.bam import get_bam_documents
from connectors.hcp import get_hcp_documents
from connectors.mef import get_mef_documents
from connectors.imf import get_imf_documents
from connectors.worldbank import get_worldbank_documents


def get_all_documents():

    docs = []

    try:
        docs.extend(get_bam_documents())
    except Exception as e:
        print(e)

    try:
        docs.extend(get_hcp_documents())
    except Exception as e:
        print(e)

    try:
        docs.extend(get_mef_documents())
    except Exception as e:
        print(e)

    try:
        docs.extend(get_imf_documents())
    except Exception as e:
        print(e)

    try:
        docs.extend(get_worldbank_documents())
    except Exception as e:
        print(e)

    return docs
