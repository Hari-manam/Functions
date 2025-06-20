import streamlit as st
from qdrant_client import QdrantClient
import os
from dotenv import load_dotenv
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

load_dotenv()

st.title("🔍 RAG Chatbot with Qdrant + Flan-T5")

# 🔗 Qdrant connection and debug info
try:
    client = QdrantClient(
        url=os.getenv("QDRANT_URL"),
        api_key=os.getenv("QDRANT_API_KEY")
    )
    info = client.get_collection("rag_collection")
    st.success("✅ Connected to Qdrant!")
    st.json(info.model_dump())
    st.markdown("---")
except Exception as e:
    st.error("❌ Qdrant connection failed!")
    st.text(str(e))
    st.markdown("---")

# 💬 Chatbot input/output
user_query = st.text_input("Ask your question:")

if st.button("Get Answer"):
    if user_query.strip() == "":
        st.warning("Please enter a question.")
    else:
        st.write("🧠 Generating answer...")

        # ✅ Use a smaller model that works on Streamlit
        model_id = "google/flan-t5-base"
        tokenizer = AutoTokenizer.from_pretrained(model_id)
        model = AutoModelForSeq2SeqLM.from_pretrained(model_id)

        # Format input & generate
        input_ids = tokenizer(user_query, return_tensors="pt").input_ids
        outputs = model.generate(input_ids, max_new_tokens=100)
        response = tokenizer.decode(outputs[0], skip_special_tokens=True)

        # Display
        st.success("✅ Answer:")
        st.write(response.strip())
