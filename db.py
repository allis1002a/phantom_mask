from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URL = "mongodb://root:example@localhost:27017/?authSource=admin"
client = AsyncIOMotorClient(MONGO_URL)
db = client["maskstore"]

pharmacies_collection = db["pharmacies"]
users_collection = db["users"]
transactions_collection = db["transactions"]

