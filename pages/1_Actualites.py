try:
    from connectors.aggregator import get_all_documents

    data = get_all_documents()

except Exception as e:
    st.error(f"Erreur chargement données : {e}")
    data = []
