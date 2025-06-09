from crewai import Agent
from app.services.llm_service import LLMService
from app.config.settings import settings

class OrderProcessingAgent:
    def __init__(self):
        self.llm_service = LLMService()
        
    def create_agent(self):
        return Agent(
            role="معالج الطلبات",
            goal="معالجة وتنظيم طلبات العملاء بدقة وكفاءة",
            backstory=f"""
            أنت خبير في معالجة الطلبات في شركة {settings.COMPANY_NAME}.
            مهمتك هي تحليل رسائل العملاء واستخراج معلومات الطلبات منها.
            أنت دقيق في التفاصيل وتتأكد من اكتمال جميع المعلومات المطلوبة.
            """,
            verbose=True,
            allow_delegation=False,
            llm=self.llm_service.llm
        )
