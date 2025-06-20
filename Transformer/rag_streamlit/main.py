import streamlit as st
from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
import torch
import os
from dotenv import load_dotenv

load_dotenv()

st.title("🔍 RAG Chatbot with Qdrant + Flan-T5")

# Step 1: Connect to Qdrant
try:
    client = QdrantClient(
        url=os.getenv("QDRANT_URL"),
        api_key=os.getenv("QDRANT_API_KEY")
    )
    info = client.get_collection("rag_collection")
    st.success("✅ Connected to Qdrant!")
    st.json(info.model_dump())
except Exception as e:
    st.error("❌ Qdrant connection failed!")
    st.text(str(e))

st.markdown("---")

# Step 2: Input box
user_query = st.text_input("Ask your question:")

if st.button("Get Answer"):
    if user_query.strip() == "":
        st.warning("Please enter a question.")
    else:
        st.write("📥 Retrieving relevant context...")

        # Step 3: Load embedding model and get query vector
        embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
        query_vector = embedding_model.encode(user_query).tolist()

        # Step 4: Retrieve top-k documents from Qdrant
        search_result = client.search(
            collection_name="rag_collection",
            query_vector=query_vector,
            limit=3
        )

        context = "\n".join([hit.payload.get("text", "") for hit in search_result])
        st.write("🧠 Retrieved context:")
        st.info(context)

        # Step 5: Load FLAN-T5 model
        st.write("💬 Generating answer...")
        model_id = "google/flan-t5-base"
        tokenizer = AutoTokenizer.from_pretrained(model_id)
        model = AutoModelForSeq2SeqLM.from_pretrained(model_id)

        # Step 6: Format prompt with context
        prompt = f"Context:\n{context}\n\nQuestion: {user_query}\nAnswer:"
        input_ids = tokenizer(prompt, return_tensors="pt").input_ids
        outputs = model.generate(input_ids, max_new_tokens=150)
        response = tokenizer.decode(outputs[0], skip_special_tokens=True)

        # Step 7: Display
        st.success("✅ Answer:")
        st.write(response.strip())
