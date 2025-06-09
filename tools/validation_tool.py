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