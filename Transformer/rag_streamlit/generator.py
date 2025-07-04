import openai
import os

openai.api_key = os.getenv("FIREWORKS_API_KEY")
openai.base_url = "https://api.fireworks.ai/inference/v1/"

def generate_answer(context, question):
    prompt = (
        "You are a Supreme Court legal expert. Based on the following context and the user's question, provide a specific, context-grounded, and conclusive answer. "
        "Do NOT provide generic legal frameworks or generalities. Always quote or reference the actual context provided, and synthesize a clear, practical conclusion. "
        "If the context is silent or ambiguous, explain what can and cannot be inferred, and still provide your best legal conclusion based on the context and standard legal principles. "
        "Use bullet points or a numbered list for key points, and always end with a clear, direct answer to the user's question.\n\n"
        f"Context:\n{context}\n\n"
        f"Question: {question}\n\n"
        "Answer:"
    )
    client = openai.OpenAI(
        api_key=openai.api_key,
        base_url=openai.base_url
    )
    response = client.chat.completions.create(
        model="accounts/fireworks/models/llama4-scout-instruct-basic",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content.strip()