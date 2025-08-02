from pydantic import BaseModel, Field
from datetime import datetime

class Transaction(BaseModel):
    user_name: str
    pharmacy_name: str
    mask_name: str
    transaction_amount: float
    transaction_date: datetime

class TransactionSummary(BaseModel):
    total_masks: int
    total_amount: float
