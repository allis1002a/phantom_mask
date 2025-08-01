import json
import re
from pathlib import Path
from datetime import datetime

base_dir = Path("data")
raw_dir = base_dir / "raw"
out_dir = base_dir / "mongodb_data"
out_dir.mkdir(parents=True, exist_ok=True)

with open(raw_dir / "pharmacies.json", encoding="utf-8") as f:
    pharmacies_raw = json.load(f)

with open(raw_dir / "users.json", encoding="utf-8") as f:
    users_raw = json.load(f)

# Create a NEW pharmacies.json
# day: Mon - Wed -> ["Mon", "Tue", "Wed"]
day_order = ["Mon", "Tue", "Wed", "Thur", "Fri", "Sat", "Sun"]
def expand_days(day_str):
    parts = [s.strip() for s in day_str.strip().split(",")]
    days = []
    for part in parts:
        if "-" in part:
            start_day, end_day = [d.strip() for d in part.split("-")]
            start_idx = day_order.index(start_day)
            end_idx = day_order.index(end_day)
            if start_idx <= end_idx:
                days.extend(day_order[start_idx:end_idx + 1])
        else:
            days.append(part)
    return days

# hours: 08:00 - 17:00 ->  {start: 08:00, end:17:00}
def parse_hours(opening_hours):
    result = {}
    segments = [seg.strip() for seg in opening_hours.split("/")]
    for segment in segments:
        match = re.match(r"([A-Za-z ,\-]+)\s+(\d{2}:\d{2})\s*-\s*(\d{2}:\d{2})", segment)
        if match:
            days_str, start, end = match.groups()
            days = expand_days(days_str)
            for day in days:
                result.setdefault(day, []).append({"start": start, "end": end})
    return result

# UPDATE a pharmacies.json
normalized_pharmacies = []
for pharmacy in pharmacies_raw:
    normalized_pharmacies.append({
        "pharmacy_name": pharmacy["name"],
        "cash_balance": pharmacy["cashBalance"],
        "openinghours": parse_hours(pharmacy["openingHours"]),
        "masks": pharmacy["masks"]  
    })

# Create transactions.json from users.json
users_out = []
transactions_out = []

for user in users_raw:
    users_out.append({
        "user_name": user["name"],
        "cash_balance": user["cashBalance"]
    })

    for tx in user.get("purchaseHistories", []):
        transactions_out.append({
            "user_name": user["name"],
            "pharmacy_name": tx["pharmacyName"],
            "mask_name": tx["maskName"],
            "transaction_amount": tx["transactionAmount"],
            "transaction_date": datetime.strptime(tx["transactionDate"], "%Y-%m-%d %H:%M:%S").isoformat()
        })

# Output
with open(out_dir / "pharmacies.json", "w", encoding="utf-8") as f:
    json.dump(normalized_pharmacies, f, indent=2, ensure_ascii=False)

with open(out_dir / "users.json", "w", encoding="utf-8") as f:
    json.dump(users_out, f, indent=2, ensure_ascii=False)

with open(out_dir / "transactions.json", "w", encoding="utf-8") as f:
    json.dump(transactions_out, f, indent=2, ensure_ascii=False)

print("All files exported to:", out_dir)
