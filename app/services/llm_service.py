from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
from app.config.settings import settings
import logging

logger = logging.getLogger(__name__)

class LLMService:
    def __init__(self):
        self.llm = self._initialize_llm()
    
    def _initialize_llm(self):
        """تهيئة نموذج اللغة حسب المتوفر"""
        try:
            if settings.LLM_PROVIDER == "google":
                return ChatGoogleGenerativeAI(
                    model="gemini-pro",
                    google_api_key=settings.GOOGLE_API_KEY,
                    temperature=0.7,
                    convert_system_message_to_human=True
                )
            elif settings.LLM_PROVIDER == "groq":
                # Note: For Groq, you'd need to use their specific client
                # This is a placeholder - implement based on Groq's SDK
                return ChatOpenAI(
                    model_name="mixtral-8x7b-32768",
                    openai_api_key=settings.GROQ_API_KEY,
                    openai_api_base="https://api.groq.com/openai/v1",
                    temperature=0.7
                )
            elif settings.LLM_PROVIDER == "openai":
                return ChatOpenAI(
                    model_name="gpt-3.5-turbo",
                    openai_api_key=settings.OPENAI_API_KEY,
                    temperature=0.7
                )
            else:
                raise ValueError("No valid LLM provider configured")
                
        except Exception as e:
            logger.error(f"Failed to initialize LLM: {e}")
            raise
    
    def generate_response(self, system_prompt: str, user_message: str) -> str:
        """توليد رد من نموذج اللغة"""
        try:
            messages = [
                SystemMessage(content=system_prompt),
                HumanMessage(content=user_message)
            ]
            
            response = self.llm.invoke(messages)
            return response.content
            
        except Exception as e:
            logger.error(f"Error generating LLM response: {e}")
            return "عذراً، حدث خطأ في معالجة طلبك. يرجى المحاولة مرة أخرى."
    
    def extract_order_info(self, customer_message: str) -> str:
        """استخراج معلومات الطلب من رسالة العميل"""
        system_prompt = f"""
أنت مساعد ذكي لشركة {settings.COMPANY_NAME} المتخصصة في {settings.BUSINESS_DESCRIPTION}.

مهمتك هي استخراج معلومات الطلب من رسالة العميل وتحويلها إلى JSON منظم.

يجب أن يحتوي الـ JSON على:
1. customer_info: اسم العميل، رقم الهاتف، البريد الإلكتروني، العنوان
2. order_items: قائمة بالمنتجات المطلوبة مع الكمية والسعر
3. notes: أي ملاحظات إضافية
4. needs_clarification: true/false إذا كانت هناك معلومات ناقصة

مثال للتنسيق المطلوب:
{{
    "customer_info": {{
        "name": "أحمد محمد",
        "phone": "01234567890",
        "email": "ahmed@example.com",
        "address": "القاهرة - المعادي"
    }},
    "order_items": [
        {{
            "product_name": "منتج أ",
            "quantity": 2,
            "unit_price": 100.0
        }}
    ],
    "notes": "ملاحظات إضافية",
    "needs_clarification": false
}}

إذا كانت المعلومات غير كاملة، ضع needs_clarification: true واذكر المعلومات المطلوبة.
"""
        
        return self.generate_response(system_prompt, customer_message)
    
    def generate_customer_response(self, context: str, customer_message: str) -> str:
        """توليد رد احترافي للعميل"""
        system_prompt = f"""
أنت مندوب خدمة عملاء محترف لشركة {settings.COMPANY_NAME}.

الشركة متخصصة في: {settings.BUSINESS_DESCRIPTION}

سلوكك يجب أن يكون:
- محترف ومهذب
- ودود ومساعد
- واضح ومباشر
- يركز على حل مشاكل العملاء
- يطرح أسئلة محددة عند الحاجة لمعلومات إضافية

استجب لرسالة العميل بشكل طبيعي ومهني، وساعده في إتمام طلبه.

السياق السابق للمحادثة: {context}
"""
        
        return self.generate_response(system_prompt, customer_message)
    
    def validate_order_completeness(self, order_data: str) -> str:
        """التحقق من اكتمال بيانات الطلب"""
        system_prompt = """
تحقق من اكتمال بيانات الطلب التالية:

يجب أن تحتوي على:
1. معلومات العميل (الاسم ورقم الهاتف على الأقل)  
2. تفاصيل المنتجات المطلوبة
3. الكمية لكل منتج

أجب بـ JSON يحتوي على:
- is_complete: true/false
- missing_info: قائمة بالمعلومات الناقصة
- suggested_questions: أسئلة مقترحة لطرحها على العميل
"""
        
        return self.generate_response(system_prompt, order_data)