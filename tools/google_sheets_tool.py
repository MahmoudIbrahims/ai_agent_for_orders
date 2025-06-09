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