from crewai import Agent
from app.services.llm_service import LLMService
from app.config.settings import settings

class CustomerServiceAgent:
    def __init__(self):
        self.llm_service = LLMService()
        
    def create_agent(self):
        return Agent(
            role="مندوب خدمة العملاء",
            goal="تقديم خدمة عملاء استثنائية والتفاعل مع العملاء بشكل احترافي",
            backstory=f"""
            أنت مندوب خدمة عملاء محترف تعمل في شركة {settings.COMPANY_NAME}.
            لديك خبرة واسعة في التعامل مع العملاء وحل مشاكلهم.
            أنت معروف بالود والاحترافية والقدرة على فهم احتياجات العملاء.
            """,
            verbose=True,
            allow_delegation=False,
            llm=self.llm_service.llm
        )
