
import streamlit as st
from qdrant_client import QdrantClient
import os
from dotenv import load_dotenv

load_dotenv()

st.title("🔍 RAG Chatbot with Qdrant + Zephyr")

try:
    client = QdrantClient(
        url=os.getenv("QDRANT_URL"),
        api_key=os.getenv("QDRANT_API_KEY")
    )

    info = client.get_collection("rag_collection")
    st.success("✅ Successfully connected to Qdrant and fetched collection!")
    st.json(info.model_dump())  # <-- shows full details
    # Add this after successful Qdrant connection display
st.markdown("---")
st.header("💬 Ask a Question to Zephyr Chatbot")

user_query = st.text_input("Ask your question:")

if st.button("Get Answer"):
    if user_query.strip() == "":
        st.warning("Please enter a question.")
    else:
        st.write("🔄 Generating answer with Zephyr...")

        # Load the Zephyr model (or your choice of HF model)
        from transformers import AutoModelForCausalLM, AutoTokenizer
        import torch

        model_id = "HuggingFaceH4/zephyr-7b-beta"  # adjust if yours is different
        tokenizer = AutoTokenizer.from_pretrained(model_id)
        model = AutoModelForCausalLM.from_pretrained(model_id, torch_dtype=torch.float16).to("cuda" if torch.cuda.is_available() else "cpu")

        prompt = f"<|user|>\n{user_query}\n<|assistant|>\n"
        input_ids = tokenizer(prompt, return_tensors="pt").input_ids.to(model.device)
        outputs = model.generate(input_ids, max_new_tokens=100, do_sample=True)
        response = tokenizer.decode(outputs[0], skip_special_tokens=True)

        st.success("✅ Answer:")
        st.write(response.split("<|assistant|>\n")[-1].strip())

except Exception as e:
    st.error("❌ Qdrant connection failed!")
    st.text(str(e))

