from pydantic import BaseModel, Field

class User(BaseModel):
    user_name: str
    cash_balance: float

class TopTransactionUser(BaseModel):
    user_name: str
    total_amount: float

