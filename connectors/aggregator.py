from connectors.hcp import get_hcp_documents
from connectors.mef import get_mef_documents
from connectors.imf import get_imf_documents
from connectors.worldbank import get_worldbank_documents
from connectors.oecd import get_oecd_documents
from connectors.bam import get_bam_documents


def get_all_documents():

    docs = []

    for source in [
        get_hcp_documents,
        get_mef_documents,
        get_imf_documents,
        get_worldbank_documents,
        get_oecd_documents,
        get_bam_documents
    ]:

        try:
            docs.extend(source())

        except Exception as e:

            print(
                f"{source.__name__}: {e}"
            )

    return docs
