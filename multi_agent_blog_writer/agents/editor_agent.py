from huggingface_hub import InferenceClient
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get the Hugging Face API token
hf_token = os.getenv("HUGGINGFACEHUB_API_TOKEN")
if not hf_token:
    raise ValueError("HUGGINGFACEHUB_API_TOKEN not found in environment variables. Please check your .env file.")

# Initialize the inference client with the Zephyr-7B model
client = InferenceClient(model="HuggingFaceH4/zephyr-7b-beta", token=hf_token)

def write_paragraph(step, topic):
    """
    Generate a detailed, factual, and engaging paragraph about the given topic for the given step.
    """
    try:
        prompt = f"Write a detailed, factual, and engaging paragraph about {topic}, focusing on: {step}"
        response = client.text_generation(prompt, max_new_tokens=200, temperature=0.7)
        return response.strip()
    except Exception as e:
        print(f"Error generating content: {str(e)}")
        return f"Error: Could not generate content for {step}. Please check your API token and permissions."
    
def generate_text(prompt, max_tokens=100):
    """
    General-purpose text generation helper.
    """
    try:
        response = client.text_generation(prompt, max_new_tokens=max_tokens, temperature=0.7)
        return response.strip()
    except Exception as e:
        print(f"Error generating text: {str(e)}")
        return "Error: Could not generate output."

def optimize_content(content):
    """
    Optimize and polish the generated content.
    """
    return content.strip() + "\n\n"