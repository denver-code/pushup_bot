import motor.motor_asyncio
from dotenv import load_dotenv
import os

load_dotenv()

client = motor.motor_asyncio.AsyncIOMotorClient(os.getenv('database', "mongodb://127.0.0.1:27017"))

db = client["pushup_bot"]
users = db["users"]


async def insert_db(_db, data):
    return await globals()[_db].insert_one(data)


async def find_one_query(_db, query):
    return await globals()[_db].find_one(query)


async def find_query(_db, query):
    cursor = globals()[_db].find(query)
    return await cursor.to_list(length=1000)


async def update_db(_db, old_data, new_data):
    return await globals()[_db].update_one(old_data, {"$set": new_data}, upsert=True)


async def delete__db(_db, obj):
    await globals()[_db].delete_one(obj)
    