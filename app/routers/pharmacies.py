from fastapi import APIRouter, Query, HTTPException
from app.db import pharmacies_collection
from datetime import datetime
from app.models.pharmacy_model import PharmacyOpeningHour, Mask, PharmacyWithPriceMasks
from app.models.pharmacy_model import MaskCountCondition
from typing import List
import re

router = APIRouter()

# List all pharmacies open at a specific time and on a day of the week if requested.
@router.get("/open", response_model=List[PharmacyOpeningHour])
async def get_open_pharmacies(day: str = Query(...), time: str = Query(...)):
    try:
        input_time = datetime.strptime(time, "%H:%M").time()
        day = day.strip().capitalize()
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid time format. Use HH:MM")

    valid_days = {"Mon", "Tue", "Wed", "Thur", "Fri", "Sat", "Sun"}
    if day not in valid_days:
        raise HTTPException(status_code=400, detail="Invalid day of the week")

    result = []
    cursor = pharmacies_collection.find()
    for doc in await cursor.to_list(length=1000):
        time_blocks = doc.get("openinghours", {}).get(day, [])
        for block in time_blocks:
            start = datetime.strptime(block["start"], "%H:%M").time()
            end = datetime.strptime(block["end"], "%H:%M").time()

            if start <= end:
                if start <= input_time <= end:
                    break
            else:  # midnight issue
                if input_time >= start or input_time <= end:
                    break
        else:
            continue  
        # doc.pop("_id", None) ObjectId issues
        result.append(doc)
    return result

# List all masks sold by a given pharmacy, sorted by mask name or price.
# list masks from a given pharmacy
# and then sorted by mask name or prcie
@router.get("/{pharmacy_name}/masks", response_model=List[Mask])
async def get_pharmacy_masks(pharmacy_name: str):
    doc = await pharmacies_collection.find_one({"pharmacy_name": pharmacy_name})
    if not doc:
        raise HTTPException(status_code=404, detail="Pharmacy not found")

    masks = sorted(doc.get("masks", []), key=lambda m: m["name"])
    return masks

# List all pharmacies with more or fewer than x mask products within a specific price range.
# n mask products within a specific price range
# more or fewer
# list pharmacies name , matched masks
@router.get("/masks/by-price-range", response_model=List[PharmacyWithPriceMasks], summary="Get pharmacies by mask price range and count condition")
async def get_pharmacies_by_mask_price(
    min_price: float = Query(...),
    max_price: float = Query(...),
    condition: MaskCountCondition = Query(...),
    count: int = Query(...)
):
    results = []

    cursor = pharmacies_collection.find()
    for doc in await cursor.to_list(length=1000):
        masks_in_range = [
            m for m in doc.get("masks", [])
            if min_price <= m["price"] <= max_price
        ]

        if len(masks_in_range) > 0 and ( # masks_in_range is not empty
            (condition == "more" and len(masks_in_range) > count) or
            (condition == "fewer" and len(masks_in_range) < count)
        ):
            results.append({
                "pharmacy_name": doc["pharmacy_name"],
                "matched_masks": masks_in_range
            })

    return results 
