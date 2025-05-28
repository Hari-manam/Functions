from huggingface_hub import InferenceClient
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get token
token = os.getenv("HUGGINGFACEHUB_API_TOKEN")
print("Token found:", "Yes" if token else "No")
print("Token starts with:", token[:10] + "..." if token else "No token")

# Test the token
try:
    client = InferenceClient(token=token)
    # Try a simple text generation
    response = client.text_generation(
        "Write one sentence about Python programming.",
        max_new_tokens=50
    )
    print("\nTest successful! Response:", response)
except Exception as e:
    print("\nError occurred:", str(e)) 