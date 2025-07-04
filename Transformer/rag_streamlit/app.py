import streamlit as st
import requests

st.title("Multi-RAG Chatbot")

rag_type = st.selectbox("Choose RAG type", ["standard", "fusion", "speculative", "corrective", "agentic"])
question = st.text_input("Ask your question:")

if st.button("Ask"):
    payload = {"query": question, "rag_type": rag_type}
    response = requests.post("http://127.0.0.1:8000/rag", json=payload)
    if response.status_code == 200:
        result = response.json()
        st.write("Answer:", result.get("answer"))
        st.write("Docs:", result.get("docs"))
    else:
        st.error("Error: " + response.text)