import os
from openai import OpenAI
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

def get_perplexity_client():
    """
    Returns an OpenAI client configured for Perplexity API.
    """
    api_key = os.getenv("PERPLEXITY_API_KEY")
    if not api_key:
        raise ValueError("PERPLEXITY_API_KEY environment variable is not set.")

    return OpenAI(
        api_key=api_key,
        base_url="https://api.perplexity.ai"
    )

def get_perplexity_llm():
    """
    Returns a LangChain ChatOpenAI instance configured for Perplexity API.
    """
    api_key = os.getenv("PERPLEXITY_API_KEY")
    if not api_key:
        raise ValueError("PERPLEXITY_API_KEY environment variable is not set.")

    print(f"Initializing ChatOpenAI with base_url=https://api.perplexity.ai and model=sonar-pro")
    return ChatOpenAI(
        model="sonar-pro",
        openai_api_key=api_key,
        openai_api_base="https://api.perplexity.ai"
    )
