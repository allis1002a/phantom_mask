from fastapi import APIRouter, HTTPException
from datetime import datetime
from app.db import users_collection, pharmacies_collection, transactions_collection
from app.models.transactioon_model import PurchaseRequest

router = APIRouter()

# user buy a mask -> user_name, mask_name, pharmacy_name, timestamp (= one transaction)
# price -> mask_name, pharmacy_name, price
# User cash_balance -> cash_balance - price
# Pharmacy cash_balance -> cash_balance + price
# Update User and Pharmacy cash_balance [negative number is allowed]
# [ignore] User cash_balance is enough or not -> user cash balance < total_cost(sum price)

@router.post("/purchase", status_code=201)
async def purchase_masks(purchase: PurchaseRequest):
    user = await users_collection.find_one({"user_name": purchase.user_name})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    total_cost = 0
    transactions = []

    for item in purchase.items:
        pharmacy = await pharmacies_collection.find_one({"pharmacy_name": item.pharmacy_name})
        if not pharmacy:
            raise HTTPException(
                status_code=404, detail=f"Pharmacy '{item.pharmacy_name}' not found")

        mask = next((m for m in pharmacy.get("masks", [])
                    if m["name"] == item.mask_name), None)
        if not mask:
            raise HTTPException(
                status_code=404, detail=f"Mask '{item.mask_name}' not found in '{item.pharmacy_name}'")

        price = mask["price"]
        total_cost += price
        transactions.append({
            "user_name": purchase.user_name,
            "pharmacy_name": item.pharmacy_name,
            "mask_name": item.mask_name,
            "price": price,
            "timestamp": datetime.utcnow()
        })

    if user["cash_balance"] < total_cost:
        raise HTTPException(status_code=400, detail="Insufficient balance")

    await users_collection.update_one(
        {"user_name": purchase.user_name},
        {"$inc": {"cash_balance": -total_cost}}
    )

    for tx in transactions:
        await pharmacies_collection.update_one(
            {"pharmacy_name": tx["pharmacy_name"]},
            {"$inc": {"cash_balance": tx["price"]}}
        )

    await transactions_collection.insert_many(transactions)

    response = {
        "status": "success",
        "total_spent": total_cost,
    }

    return response
