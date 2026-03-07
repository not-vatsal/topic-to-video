import os
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from google import genai
load_dotenv()


client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

models = client.models.list()

for m in models:
    print(m.name)
def get_google_llm():
    """Returns a LangChain LLM instance configured for Google Gemini."""
    api_key = os.getenv("GEMINI_API_KEY")
    
    return ChatGoogleGenerativeAI(
        model="model/gemini-2.5-flash", # Or gemini-1.5-pro
        google_api_key=api_key
    )
print(get_google_llm())
print([m.name for m in client.models.list()])

