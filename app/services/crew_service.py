from crewai import Crew, Task
from agents.customer_service_agent import CustomerServiceAgent
from agents.order_processing_agent import OrderProcessingAgent  
from agents.data_entry_agent import DataEntryAgent
from tools.google_sheets_tool import GoogleSheetsTool
from tools.validation_tool import ValidationTool
import logging

logger = logging.getLogger(__name__)

class CrewService:
    def __init__(self):
        # Initialize agents
        self.customer_service_agent = CustomerServiceAgent().create_agent()
        self.order_processing