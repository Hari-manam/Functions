import streamlit as st
from qdrant_client import QdrantClient
from qdrant_client.http.models import Filter, FieldCondition, MatchValue, SearchParams
import os
from dotenv import load_dotenv
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

# Load environment variables
load_dotenv()

st.title("🔍 RAG Chatbot with Qdrant + Falcon-RW-1B")

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
    st.stop()

st.markdown("---")

# Step 2: Load Falcon-RW-1B model and tokenizer
@st.cache_resource
def load_falcon():
    model_id = "tiiuae/falcon-rw-1b"
    tokenizer = AutoTokenizer.from_pretrained(model_id)
    model = AutoModelForCausalLM.from_pretrained(model_id)
    return tokenizer, model

tokenizer, model = load_falcon()

# Step 3: User Input
user_query = st.text_input("💬 Ask a question:")

if st.button("Get Answer"):
    if not user_query.strip():
        st.warning("Please enter a valid question.")
        st.stop()

    # Step 4: Embed user query using a placeholder (since we don't embed here)
    # For real RAG, embed and search vector DB — simplified for now
    st.write("📥 Retrieving relevant context...")

    search_result = client.search(
        collection_name="rag_collection",
        query_vector=tokenizer(user_query, return_tensors="pt").input_ids[0].tolist(),
        limit=3,
        search_params=SearchParams(hnsw_ef=128, exact=False)
    )

    context_chunks = [hit.payload.get("text", "") for hit in search_result]
    context = "\n".join(context_chunks)

    if not context:
        st.warning("No relevant context found. Answering directly...")
        context = "No context available."

    # Step 5: Build Prompt
    prompt = f"""You are a helpful AI assistant. Use the context to answer the question.

Context:
{context}

Question:
{user_query}

Answer:"""

    # Step 6: Generate Answer
    st.write("🧠 Generating answer using Falcon-RW-1B...")
    input_ids = tokenizer(prompt, return_tensors="pt").input_ids
    outputs = model.generate(input_ids, max_new_tokens=150)
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)

    # Step 7: Show Answer
    st.success("✅ Answer:")
    st.write(response.split("Answer:")[-1].strip())
