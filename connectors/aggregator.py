from connectors.bam import get_bam_documents
from connectors.imf import get_imf_documents
from connectors.worldbank import get_worldbank_documents


def get_all_documents():

    docs = []

    docs.extend(get_bam_documents())
    docs.extend(get_imf_documents())
    docs.extend(get_worldbank_documents())

    return docs
