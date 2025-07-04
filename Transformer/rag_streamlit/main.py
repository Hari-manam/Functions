import streamlit as st
from retriever import fusion_retrieve, retrieve, speculative_retrieve, corrective_retrieve, agentic_retrieve, expanded_corrective_retrieve, unified_retrieve
from generator import generate_answer

st.title("📚 RAG Chatbot with Qdrant")

query = st.text_input("Ask your question:")
# Removed the number of chunks slider
# top_k = st.slider("Number of chunks to retrieve", min_value=1, max_value=20, value=8)
top_k = 8  # Default value, not shown in UI

embedding_model = st.selectbox(
    "Select embedding model",
    [
        "all-MiniLM-L6-v2",
        "paraphrase-MiniLM-L6-v2"
        # Uncomment below if you want to try a legal-specific model and have it installed (must be 384-dim):
        # "nlpaueb/legal-bert-base-uncased"
    ]
)

rag_strategy = st.selectbox(
    "Select RAG strategy",
    ["Standard", "Fusion", "Speculative", "Corrective", "Expanded Corrective", "Agentic"]
)

# Add backend selection
backends = st.multiselect(
    "Select vector backends",
    ["qdrant", "pinecone", "milvus", "mongodb"],
    default=["qdrant"]
)

similarity_threshold = 0.6
if rag_strategy == "Corrective":
    similarity_threshold = st.slider("Corrective RAG: Similarity threshold (0.0-1.0)", min_value=0.0, max_value=1.0, value=0.6, step=0.01)

# Add a debug checkbox for developer use
show_debug = st.sidebar.checkbox("Show retrieved chunks (debug)")

if st.button("Get Answer") and query:
    # Check for greetings
    if query.strip().lower() in ["hi", "hello", "hey", "greetings"]:
        st.markdown("**Answer:** Hello! How can I help you today?")
    else:
        if rag_strategy == "Fusion":
            # Use unified_retrieve for multi-backend support
            docs = unified_retrieve(query, top_k=top_k, embedding_model=embedding_model, backends=backends)
        elif rag_strategy == "Speculative":
            docs = speculative_retrieve(query, top_k=top_k, embedding_model=embedding_model)
        elif rag_strategy == "Corrective":
            docs = corrective_retrieve(query, top_k=top_k, similarity_threshold=similarity_threshold, embedding_model=embedding_model)
        elif rag_strategy == "Expanded Corrective":
            docs = expanded_corrective_retrieve(query, top_k=top_k, similarity_threshold=similarity_threshold, embedding_model=embedding_model)
        elif rag_strategy == "Agentic":
            docs = agentic_retrieve(query, top_k=top_k, embedding_model=embedding_model)
        else:
            docs = retrieve(query, top_k=top_k, embedding_model=embedding_model)
        if not docs:
            st.markdown("<span style='color:red'><b>No relevant information found in the context to answer your question.</b></span>", unsafe_allow_html=True)
        else:
            # Debug output: show retrieved chunks if checkbox is enabled
            if show_debug:
                st.markdown("**[DEBUG] Retrieved Chunks:**")
                for i, doc in enumerate(docs):
                    st.markdown(f"<details><summary>Chunk {i+1} - `{doc.get('filename', 'unknown')}` (chunk {doc.get('chunk_id', '?')})</summary><pre style='white-space:pre-wrap'>{doc['text']}</pre></details>", unsafe_allow_html=True)
            context = "\n".join([doc["text"] for doc in docs])
            answer = generate_answer(context, query)
            st.markdown(f"**Answer:** {answer}")
            # Show sources
            st.markdown("**Sources:**")
            for doc in docs:
                st.markdown(f"- `{doc.get('filename', 'unknown')}` (source: {doc.get('source', 'unknown')})")
