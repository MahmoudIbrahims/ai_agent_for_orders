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

# agents/order_processing_agent.py
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

# agents/data_entry_agent.py
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

# tools/google_sheets_tool.py
from crewai_tools import BaseTool
from app.services.google_sheets_service import GoogleSheetsService
from app.models.order_model import Order
import json

class GoogleSheetsTool(BaseTool):
    name: str = "Google Sheets Tool"
    description: str = "أداة لحفظ الطلبات في Google Sheets"
    
    def __init__(self):
        super().__init__()
        self.sheets_service = GoogleSheetsService()
    
    def _run(self, order_json: str) -> str:
        """حفظ الطلب في Google Sheets"""
        try:
            order_data = json.loads(order_json)
            # Convert to Order model and save
            # This is a simplified version - you'd need to properly parse the JSON
            # and create the Order object
            result = self.sheets_service.add_order(order_data)
            
            if result:
                return "تم حفظ الطلب بنجاح في Google Sheets"
            else:
                return "فشل في حفظ الطلب"
                
        except Exception as e:
            return f"خطأ في حفظ الطلب: {str(e)}"

# tools/validation_tool.py
from crewai_tools import BaseTool
import json
import re

class ValidationTool(BaseTool):
    name: str = "Validation Tool"
    description: str = "أداة للتحقق من صحة بيانات الطلبات"
    
    def _run(self, data: str) -> str:
        """التحقق من صحة البيانات"""
        try:
            order_data = json.loads(data)
            errors = []
            
            # Check customer info
            customer_info = order_data.get('customer_info', {})
            if not customer_info.get('name'):
                errors.append("اسم العميل مطلوب")
            
            if not customer_info.get('phone'):
                errors.append("رقم الهاتف مطلوب")
            else:
                phone = customer_info.get('phone')
                if not re.match(r'^01[0-9]{9}$', phone):
                    errors.append("رقم الهاتف غير صحيح")
            
            # Check order items
            items = order_data.get('order_items', [])
            if not items:
                errors.append("يجب إضافة منتج واحد على الأقل")
            
            for item in items:
                if not item.get('product_name'):
                    errors.append("اسم المنتج مطلوب")
                if not item.get('quantity') or item.get('quantity') <= 0:
                    errors.append("كمية المنتج يجب أن تكون أكبر من صفر")
            
            if errors:
                return json.dumps({
                    "is_valid": False,
                    "errors": errors
                }, ensure_ascii=False)
            else:
                return json.dumps({
                    "is_valid": True,
                    "message": "البيانات صحيحة"
                }, ensure_ascii=False)
                
        except Exception as e:
            return json.dumps({
                "is_valid": False,
                "errors": [f"خطأ في التحقق من البيانات: {str(e)}"]
            }, ensure_ascii=False)