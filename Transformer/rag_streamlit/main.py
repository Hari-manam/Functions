
import streamlit as st
from qdrant_client import QdrantClient
import os
from dotenv import load_dotenv

load_dotenv()

st.title("🔍 Qdrant Collection Debug")

try:
    client = QdrantClient(
        url=os.getenv("QDRANT_URL"),
        api_key=os.getenv("QDRANT_API_KEY")
    )

    info = client.get_collection("rag_collection")
    st.success("✅ Successfully connected to Qdrant and fetched collection!")
    st.json(info.model_dump())  # <-- shows full details

except Exception as e:
    st.error("❌ Qdrant connection failed!")
    st.text(str(e))

