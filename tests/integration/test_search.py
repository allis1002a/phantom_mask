import pytest
from fastapi.testclient import TestClient
from app.main import app
from unittest.mock import AsyncMock, MagicMock

client = TestClient(app)

@pytest.mark.asyncio
async def test_fuzzy_search_pharmacy(mocker):
    # Mock MongoDB cursor
    fake_docs = [{"pharmacy_name": "DFW Wellness"}]
    mock_cursor = MagicMock()
    mock_cursor.to_list = AsyncMock(return_value=fake_docs)
    mock_find = MagicMock(return_value=mock_cursor)

    # Patch the collection's find method
    mocker.patch("app.db.pharmacies_collection.find", mock_find)

    response = client.get("/search/fuzzy/pharmacy-or-mask", params={
        "search_target": "pharmacy Name",
        "keyword": "DFW Wellness"
    })
    assert response.status_code == 200
    assert response.json()[0]["pharmacy_name"] == "DFW Wellness"

# @pytest.mark.asyncio
# @patch("app.db.pharmacies_collection")
# @patch("rapidfuzz.fuzz.partial_ratio")
# async def test_fuzzy_search_mask(mock_fuzz, mock_collection):
#     mock_collection.find.return_value.to_list = AsyncMock(return_value=[
#         {"pharmacy_name": "PharmaOne", "masks": [{"name": "N95 Mask"}, {"name": "Surgical Mask"}]},
#         {"pharmacy_name": "PharmaTwo", "masks": [{"name": "N95 Mask"}]}
#     ])
#     mock_fuzz.side_effect = lambda a, b: 90 if "n95" in b else 20

#     response = client.get(
#         "/fuzzy/pharmacy-or-mask",
#         params={"search_target": SearchTarget.mask, "keyword": "N95"}
#     )
#     assert response.status_code == 200
#     data = response.json()
#     assert any("N95 Mask" in r["mask_name"] for r in data)
#     assert all(r["relevance_score"] >= 0.4 for r in data)