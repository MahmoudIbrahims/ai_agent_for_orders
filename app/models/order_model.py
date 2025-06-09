from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from enum import Enum

class OrderStatus(str, Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    PROCESSING = "processing"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

class OrderItem(BaseModel):
    product_name: str = Field(..., description="اسم المنتج")
    quantity: int = Field(..., gt=0, description="الكمية")
    unit_price: float = Field(..., gt=0, description="سعر الوحدة")
    total_price: float = Field(..., description="السعر الإجمالي")

class Order(BaseModel):
    order_id: str = Field(..., description="رقم الطلب")
    customer: Customer = Field(..., description="بيانات العميل")
    items: List[OrderItem] = Field(..., description="عناصر الطلب")
    total_amount: float = Field(..., description="إجمالي المبلغ")
    status: OrderStatus = Field(default=OrderStatus.PENDING, description="حالة الطلب")
    notes: Optional[str] = Field(None, description="ملاحظات إضافية")
    created_at: datetime = Field(default_factory=datetime.now)
    
    def calculate_total(self):
        """حساب إجمالي المبلغ"""
        self.total_amount = sum(item.total_price for item in self.items)
        return self.total_amount

class OrderRequest(BaseModel):
    customer_message: str = Field(..., description="رسالة العميل")
    conversation_context: Optional[str] = Field(None, description="سياق المحادثة")