from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

def summarize_document(text):

    response = client.responses.create(
        model="gpt-5",
        input=f"""
        Summarize this document.

        {text[:10000]}
        """
    )

    return response.output_text