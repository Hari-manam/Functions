from huggingface_hub import InferenceClient
from dotenv import load_dotenv
import os

load_dotenv()
HF_TOKEN = os.getenv("HF_TOKEN")

client = InferenceClient(token=HF_TOKEN)

def generate_answer(context, question):
    prompt = f"Context: {context}\nQuestion: {question}\nAnswer:"
    response = client.text_generation(
        model="HuggingFaceH4/zephyr-7b-beta",  # ✅ Make sure model name is correct
        prompt=prompt,
        max_new_tokens=100,
        temperature=0.7
    )
    return response.strip()
