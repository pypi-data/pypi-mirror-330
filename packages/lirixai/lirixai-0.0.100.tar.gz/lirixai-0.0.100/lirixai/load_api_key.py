from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

class Settings(BaseSettings):
    groq_api_key: str
    tavily_api_key: str

    class Config:
        env_file = ".env"

# Create settings instance
settings = Settings()

# Use the API keys
print(f"Your Groq API key is: {settings.groq_api_key}")
print(f"Your Tavily API key is: {settings.tavily_api_key}")