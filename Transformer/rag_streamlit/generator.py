from huggingface_hub import InferenceClient
from dotenv import load_dotenv
import os

# Load env variables
load_dotenv()
HF_TOKEN = os.getenv("HF_TOKEN")
HF_MODEL = os.getenv("HF_MODEL")

# Initialize HF API Client
client = InferenceClient(token=HF_TOKEN)

# Generate answer using hosted model
def generate_answer(context, question):
    prompt = f"Context: {context}\nQuestion: {question}\nAnswer:"
    
    response = client.text_generation(
        model=HF_MODEL,
        prompt=prompt,
        max_new_tokens=100,
        temperature=0.7,
    )

    return response.strip()
