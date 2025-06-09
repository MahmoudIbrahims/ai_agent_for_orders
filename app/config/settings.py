import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    # Google Sheets Configuration
    GOOGLE_SHEETS_CREDENTIALS_PATH = os.getenv("GOOGLE_SHEETS_CREDENTIALS_PATH")
    GOOGLE_SHEET_ID = os.getenv("GOOGLE_SHEET_ID")
    
    # LLM Configuration
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    
    # Business Configuration
    COMPANY_NAME = os.getenv("COMPANY_NAME", "شركة الخدمات المتميزة")
    BUSINESS_DESCRIPTION = os.getenv("BUSINESS_DESCRIPTION", "نقدم خدمات متنوعة عالية الجودة")
    
    # LLM Selection (priority: Gemini > Groq > OpenAI)
    @property
    def LLM_MODEL(self):
        if self.GOOGLE_API_KEY:
            return "gemini-pro"
        elif self.GROQ_API_KEY:
            return "mixtral-8x7b-32768"
        elif self.OPENAI_API_KEY:
            return "gpt-3.5-turbo"
        else:
            raise ValueError("No LLM API key provided")
    
    @property
    def LLM_PROVIDER(self):
        if self.GOOGLE_API_KEY:
            return "google"
        elif self.GROQ_API_KEY:
            return "groq"
        elif self.OPENAI_API_KEY:
            return "openai"
        else:
            raise ValueError("No LLM API key provided")