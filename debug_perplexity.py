import os
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("PERPLEXITY_API_KEY")
print(f"Perplexity Key: {api_key[:5]}...")

llm = ChatOpenAI(
    model="sonar-pro",
    openai_api_key=api_key,
    openai_api_base="https://api.perplexity.ai"
)

try:
    print("Sending request to Perplexity...")
    response = llm.invoke("Hello, are you Perplexity?")
    print("Response received:")
    print(response.content)
except Exception as e:
    print(f"Error: {e}")
