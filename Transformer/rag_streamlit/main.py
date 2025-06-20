import streamlit as st
from qdrant_client import QdrantClient
import os
from dotenv import load_dotenv
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

# ✅ Load environment variables
load_dotenv()

st.set_page_config(page_title="RAG Chatbot", layout="centered")
st.title("🔍 RAG Chatbot with Qdrant + Flan-T5 Small")

# 🔗 Connect to Qdrant
try:
    client = QdrantClient(
        url=os.getenv("QDRANT_URL"),
        api_key=os.getenv("QDRANT_API_KEY")
    )
    info = client.get_collection("rag_collection")
    st.success("✅ Connected to Qdrant!")
    with st.expander("ℹ️ Qdrant Collection Info"):
        st.json(info.model_dump())
except Exception as e:
    st.error("❌ Qdrant connection failed!")
    st.code(str(e))

st.markdown("---")

# 💬 Chat Input
user_query = st.text_input("Ask a question:")

# Model Setup (load once)
@st.cache_resource
def load_model():
    model_id = "google/flan-t5-small"
    tokenizer = AutoTokenizer.from_pretrained(model_id)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_id)
    return tokenizer, model

tokenizer, model = load_model()

# Handle Query
if st.button("Get Answer"):
    if not user_query.strip():
        st.warning("Please enter a question.")
    else:
        st.info("🔄 Generating answer...")
        input_ids = tokenizer(user_query, return_tensors="pt").input_ids
        outputs = model.generate(input_ids, max_new_tokens=150)
        response = tokenizer.decode(outputs[0], skip_special_tokens=True)
        st.success("✅ Answer:")
        st.write(response.strip())
