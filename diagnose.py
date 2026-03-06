try:
    import sys
    from unittest.mock import MagicMock
    sys.modules["chromadb"] = MagicMock()
    print("chromadb mocked.")
except Exception as e:
    print(f"Failed to mock chromadb: {e}")

try:
    print("Importing requests...")
    import requests
    print("requests imported.")
except Exception as e:
    print(f"Failed to import requests: {e}")

try:
    print("Importing python-pptx...")
    import pptx
    print("python-pptx imported.")
except Exception as e:
    print(f"Failed to import python-pptx: {e}")

try:
    print("Importing gTTS...")
    from gtts import gTTS
    print("gTTS imported.")
except Exception as e:
    print(f"Failed to import gTTS: {e}")

try:
    print("Importing comtypes...")
    import comtypes.client
    print("comtypes imported.")
except Exception as e:
    print(f"Failed to import comtypes: {e}")

try:
    print("Importing moviepy...")
    from moviepy import VideoFileClip
    print("moviepy imported.")
except Exception as e:
    print(f"Failed to import moviepy: {e}")

try:
    print("Importing sqlite3...")
    import sqlite3
    print("sqlite3 imported.")
except Exception as e:
    print(f"Failed to import sqlite3: {e}")

try:
    print("Importing numpy...")
    import numpy
    print("numpy imported.")
except Exception as e:
    print(f"Failed to import numpy: {e}")

try:
    print("Importing pydantic...")
    import pydantic
    print("pydantic imported.")
except Exception as e:
    print(f"Failed to import pydantic: {e}")

try:
    print("Importing chromadb...")
    import chromadb
    print("chromadb imported.")
except Exception as e:
    print(f"Failed to import chromadb: {e}")

try:
    print("Importing opentelemetry...")
    import opentelemetry
    print("opentelemetry imported.")
except Exception as e:
    print(f"Failed to import opentelemetry: {e}")

try:
    print("Importing crewai.agent...")
    from crewai import Agent
    print("crewai.agent imported.")
except Exception as e:
    print(f"Failed to import crewai.agent: {e}")

try:
    print("Importing crewai.task...")
    from crewai import Task
    print("crewai.task imported.")
except Exception as e:
    print(f"Failed to import crewai.task: {e}")

try:
    print("Importing crewai.crew...")
    from crewai import Crew
    print("crewai.crew imported.")
except Exception as e:
    print(f"Failed to import crewai.crew: {e}")

try:
    print("Importing langchain_openai...")
    from langchain_openai import ChatOpenAI
    print("langchain_openai imported.")
except Exception as e:
    print(f"Failed to import langchain_openai: {e}")

print("Diagnostics complete.")
