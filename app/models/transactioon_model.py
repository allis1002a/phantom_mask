from pydantic import BaseModel, Field
from datetime import datetime
from typing import List

class Transaction(BaseModel):
    user_name: str
    pharmacy_name: str
    mask_name: str
    transaction_amount: float
    transaction_date: datetime

class TransactionSummary(BaseModel):
    total_masks: int
    total_amount: float

class PurchaseItem(BaseModel):
    pharmacy_name: str
    mask_name: str

class PurchaseRequest(BaseModel):
    user_name: str
    items: List[PurchaseItem]
