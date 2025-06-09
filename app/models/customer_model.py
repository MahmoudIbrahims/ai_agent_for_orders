from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class Customer(BaseModel):
    name: str = Field(..., description="اسم العميل")
    phone: str = Field(..., description="رقم الهاتف")
    email: Optional[str] = Field(None, description="البريد الإلكتروني")
    address: Optional[str] = Field(None, description="العنوان")
    created_at: datetime = Field(default_factory=datetime.now)


