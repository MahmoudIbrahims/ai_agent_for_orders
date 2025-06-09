import json
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from typing import List, Dict, Any
from app.config.settings import settings
from app.models.order_model import Order
import logging

logger = logging.getLogger(__name__)

class GoogleSheetsService:
    def __init__(self):
        self.credentials = None
        self.service = None
        self.sheet_id = settings.GOOGLE_SHEET_ID
        self._initialize_service()
    
    def _initialize_service(self):
        """تهيئة خدمة Google Sheets"""
        try:
            # Load credentials from service account file
            self.credentials = Credentials.from_service_account_file(
                settings.GOOGLE_SHEETS_CREDENTIALS_PATH,
                scopes=['https://www.googleapis.com/auth/spreadsheets']
            )
            
            # Build the service
            self.service = build('sheets', 'v4', credentials=self.credentials)
            logger.info("Google Sheets service initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize Google Sheets service: {e}")
            raise
    
    def create_headers_if_not_exist(self, sheet_name: str = "Orders"):
        """إنشاء العناوين في الشيت إذا لم تكن موجودة"""
        headers = [
            "رقم الطلب", "تاريخ الطلب", "اسم العميل", "رقم الهاتف", 
            "البريد الإلكتروني", "العنوان", "تفاصيل الطلبات", 
            "إجمالي المبلغ", "حالة الطلب", "ملاحظات"
        ]
        
        try:
            # Check if sheet exists and has headers
            result = self.service.spreadsheets().values().get(
                spreadsheetId=self.sheet_id,
                range=f"{sheet_name}!A1:J1"
            ).execute()
            
            if not result.get('values'):
                # Add headers
                self.service.spreadsheets().values().update(
                    spreadsheetId=self.sheet_id,
                    range=f"{sheet_name}!A1:J1",
                    valueInputOption='RAW',
                    body={'values': [headers]}
                ).execute()
                logger.info("Headers created successfully")
                
        except Exception as e:
            logger.error(f"Error creating headers: {e}")
            raise
    
    def add_order(self, order: Order, sheet_name: str = "Orders") -> bool:
        """إضافة طلب جديد إلى Google Sheets"""
        try:
            # Ensure headers exist
            self.create_headers_if_not_exist(sheet_name)
            
            # Prepare order data
            items_details = []
            for item in order.items:
                items_details.append(
                    f"{item.product_name} - الكمية: {item.quantity} - السعر: {item.unit_price} ج.م"
                )
            items_string = " | ".join(items_details)
            
            row_data = [
                order.order_id,
                order.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                order.customer.name,
                order.customer.phone,
                order.customer.email or "",
                order.customer.address or "",
                items_string,
                order.total_amount,
                order.status.value,
                order.notes or ""
            ]
            
            # Find next empty row
            result = self.service.spreadsheets().values().get(
                spreadsheetId=self.sheet_id,
                range=f"{sheet_name}!A:A"
            ).execute()
            
            next_row = len(result.get('values', [])) + 1
            
            # Add the order
            self.service.spreadsheets().values().update(
                spreadsheetId=self.sheet_id,
                range=f"{sheet_name}!A{next_row}:J{next_row}",
                valueInputOption='RAW',
                body={'values': [row_data]}
            ).execute()
            
            logger.info(f"Order {order.order_id} added successfully to Google Sheets")
            return True
            
        except Exception as e:
            logger.error(f"Error adding order to Google Sheets: {e}")
            return False
    
    def get_orders(self, sheet_name: str = "Orders") -> List[Dict[str, Any]]:
        """استرجاع جميع الطلبات من Google Sheets"""
        try:
            result = self.service.spreadsheets().values().get(
                spreadsheetId=self.sheet_id,
                range=f"{sheet_name}!A:J"
            ).execute()
            
            values = result.get('values', [])
            if not values:
                return []
            
            headers = values[0]
            orders = []
            
            for row in values[1:]:
                if len(row) >= len(headers):
                    order_dict = dict(zip(headers, row))
                    orders.append(order_dict)
            
            return orders
            
        except Exception as e:
            logger.error(f"Error retrieving orders: {e}")
            return []
    
    def update_order_status(self, order_id: str, new_status: str, sheet_name: str = "Orders") -> bool:
        """تحديث حالة طلب معين"""
        try:
            # Find the order row
            result = self.service.spreadsheets().values().get(
                spreadsheetId=self.sheet_id,
                range=f"{sheet_name}!A:I"
            ).execute()
            
            values = result.get('values', [])
            if not values:
                return False
            
            for i, row in enumerate(values):
                if i == 0:  # Skip header
                    continue
                if len(row) > 0 and row[0] == order_id:
                    # Update status in column I (index 8)
                    self.service.spreadsheets().values().update(
                        spreadsheetId=self.sheet_id,
                        range=f"{sheet_name}!I{i+1}",
                        valueInputOption='RAW',
                        body={'values': [[new_status]]}
                    ).execute()
                    
                    logger.info(f"Order {order_id} status updated to {new_status}")
                    return True
            
            return False
            
        except Exception as e:
            logger.error(f"Error updating order status: {e}")
            return False