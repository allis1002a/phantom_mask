from fastapi import APIRouter, Query
from typing import List, Dict
from datetime import datetime
from app.models.user_model import TopTransactionUser
from app.models.transactioon_model import TransactionSummary
from app.db import transactions_collection  

router = APIRouter()

# Retrieve the top x users by total transaction amount of masks within a date range.
# transaction date within a date range
# group by user, sum transaction_amount
# order by total transaction_amount (DECS)
@router.get("/top-by-amount", response_model=List[TopTransactionUser], summary="Top X users by transaction amount in date range")
async def get_top_users_by_transaction_amount(
    start_date: datetime = Query(...),
    end_date: datetime = Query(...),
    top_x: int = Query(..., gt=0, description="the top x of users")
):
    pipeline = [
        {
            "$match": {
                "transaction_date": {
                    "$gte": start_date.isoformat(),
                    "$lte": end_date.isoformat()
                }
            }
        },
        {
            "$group": {
                "_id": "$user_name",
                "total_amount": {"$sum": "$transaction_amount"}
            }
        },
        {
            "$sort": {"total_amount": -1}
        },
        {
            "$limit": top_x
        },
        { 
          "$project": {
              "_id": 0, # 0:Hide, 1:Keep original value
              "user_name": "$_id",
              "total_amount": 1 # recomand: round(2)
          }
        }
    ] 
    
    top_users = await transactions_collection.aggregate(pipeline).to_list(length=top_x)
    print(top_users)
    return top_users


# Calculate the total number of masks and the total transaction value within a date range.  
# transaction_date within a date range 
# group by mask_name, and sum it. (= the total number of masks)
# group by mask_name, and sum transaction_amount (=the total transaction value)
@router.get("/transactions/summary", response_model = List[TransactionSummary], summary="Get total masks and transaction amount in date range")
async def get_transaction_summary(
    start_date: datetime = Query(...),
    end_date: datetime = Query(...)
):
    pipeline = [
        {
            "$match": {
                "transaction_date": {
                    "$gte": start_date.isoformat(),
                    "$lte": end_date.isoformat()
                }
            }
        },
        {
            "$group": {
                "_id": None,
                "total_transactions": { "$sum": 1 },  # Assume each transaction represents one mask
                "total_amount": { "$sum": "$transaction_amount" }
            }
        },
        {
            "$project": {
                "_id": 0,
                "total_masks": "$total_transactions",
                "total_amount": 1
            }
        }
    ]

    result = await transactions_collection.aggregate(pipeline).to_list(length=1)
    return result
