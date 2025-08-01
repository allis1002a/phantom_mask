from fastapi import APIRouter, Query
from typing import List
from models.pharmacy_model import PharmacySearchResult
from models.pharmacy_model import SearchTarget
from db import pharmacies_collection
from rapidfuzz import fuzz

router = APIRouter()

# Search for pharmacies or masks by name and rank the results by relevance to the search term.
# mostly enter pharmacy name and mask name, lean to user simple searching method. [jieba/CKIP/NLTK]
# https://github.com/rapidfuzz/RapidFuzz
# choose pharmacy_name or mask_name
# use REGEX in Mongodb, then calculate simlarity score.
# order by  similarity score, mask name or pharmacy_name

@router.get("/fuzzy/pharmacy-or-mask", response_model=List[PharmacySearchResult], summary="Fuzzy search by pharmacy or mask name")
async def fuzzy_search_names(
    search_target: SearchTarget = Query(..., description="Choose pharmacy or mask"),
    keyword: str = Query(..., min_length=1)
):
    keyword_lower = keyword.lower()
    results = []

    if search_target == SearchTarget.pharmacy:
        cursor = pharmacies_collection.find(
            {"pharmacy_name": {"$regex": keyword, "$options": "i"}},
            {"pharmacy_name": 1, "_id": 0}
        )
        docs = await cursor.to_list(length=500)

        for doc in docs:
            pname = doc["pharmacy_name"]
            score = fuzz.partial_ratio(keyword_lower, pname.lower()) / 100
            if score > 0.4:
                results.append({
                    "pharmacy_name": pname,
                    "relevance_score": round(score, 3)
                })

    else:  # search_target == mask
        cursor = pharmacies_collection.find(
            {"masks.name": {"$regex": keyword, "$options": "i"}},
            {"pharmacy_name": 1, "masks": 1, "_id": 0}
        )
        docs = await cursor.to_list(length=500)

        seen_masks = set() # Recomand: mask.json

        for doc in docs:
            for mask in doc.get("masks", []):
                mname = mask["name"].strip()
                lname = mname.lower()
                if lname in seen_masks:
                    continue
                seen_masks.add(lname)

                score = fuzz.partial_ratio(keyword_lower, lname) / 100
                if score > 0.4:
                    results.append({
                        "mask_name": mname,
                        "relevance_score": round(score, 3)
                    })

    response_data = sorted(results, key=lambda r: (-r["relevance_score"], r.get("pharmacy_name", r.get("mask_name", ""))))
    return response_data
