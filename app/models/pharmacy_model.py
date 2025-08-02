from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Union
from enum import Enum

class OpeningHour(BaseModel):
    start: str = Field(..., example="08:00")
    end: str = Field(..., example="17:00")

class Mask(BaseModel):
    name: str = Field(..., example="Cotton Kiss (green) (3 per pack)")
    price: float = Field(..., example=12.5)

class PharmacyOpeningHour(BaseModel):
    pharmacy_name: str = Field(..., example="Health Mart")
    openinghours: Dict[str, List[OpeningHour]]  # "Mon": [{"start": "08:00", "end": "17:00"}]

class PharmacyWithPriceMasks(BaseModel):
    pharmacy_name: str = Field(..., example="Health Mart")
    matched_masks: List[Mask] = Field(..., description="符合價格條件的口罩清單")

class PharmacySearchResult(BaseModel):
    pharmacy_name: Optional[str] = None
    mask_name: Optional[List[Mask]] = []
    relevance_score: float

class PharmacyResult(BaseModel):
    pharmacy_name: str
    relevance_score: float

class MaskResult(BaseModel):
    mask_name: str
    relevance_score: float

PharmacyOrMaskSearchResult = Union[PharmacyResult, MaskResult]

# API condition
class MaskCountCondition(str, Enum):
    """comparing number of masks in price range"""
    more = "more"
    fewer = "fewer"

class SearchTarget(str, Enum):
    pharmacy = "pharmacy Name"
    mask = "mask Name"



