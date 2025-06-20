
import streamlit as st
from retriever import retrieve
from generator import generate_answer

st.title("📚 RAG Chatbot with Qdrant + Flan-T5")

query = st.text_input("Ask your question:")

if st.button("Get Answer"):
    with st.spinner("Retrieving..."):
        docs = retrieve(query)
        context = "\n".join(docs)
        answer = generate_answer(context, query)
        st.markdown(f"**Answer:** {answer}")
