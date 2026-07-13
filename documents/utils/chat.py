from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

def ask_gpt(question, context):

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=f"""
You are a professional document assistant.

Use only the supplied document context.

If the answer is not found in the documents,
reply:

'I could not find this information in the uploaded documents.'

Context:
{context}

Question:
{question}

Provide:
1. Direct answer
2. Supporting document name
3. Brief explanation
"""
)
    return response.output_text
