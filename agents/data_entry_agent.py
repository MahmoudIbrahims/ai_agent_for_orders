from crewai import Agent
from app.services.llm_service import LLMService
from app.config.settings import settings

class DataEntryAgent:
    def __init__(self):
        self.llm_service = LLMService()
        
    def create_agent(self):
        return Agent(
            role="مدخل البيانات",
            goal="إدخال وحفظ بيانات الطلبات في النظام بدقة",
            backstory=f"""
            أنت متخصص في إدخال البيانات في شركة {settings.COMPANY_NAME}.
            مهمتك هي حفظ طلبات العملاء في Google Sheets بشكل منظم ودقيق.
            أنت حريص على التأكد من صحة البيانات قبل حفظها.
            """,
            verbose=True,
            allow_delegation=False,
            llm=self.llm_service.llm
        )