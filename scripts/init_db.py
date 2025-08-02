import json
from pymongo import MongoClient

mongo_uri = "mongodb://root:example@mongodb:27017/?authSource=admin"
client = MongoClient(mongo_uri)

db = client["maskstore"]

# pharmacies
with open("data/mongodb_data/pharmacies.json") as f:
    pharmacies = json.load(f)
    db.pharmacies.delete_many({})
    db.pharmacies.insert_many(pharmacies)

# users
with open("data/mongodb_data/users.json") as f:
    users = json.load(f)
    db.users.delete_many({})
    db.users.insert_many(users)

# transactions
with open("data/mongodb_data/transactions.json") as f:
    transactions = json.load(f)
    db.transactions.delete_many({})
    db.transactions.insert_many(transactions)

print("MongoDB is ready")
