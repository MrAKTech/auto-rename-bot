from pymongo import MongoClient
from config import DB_URL
import sys

client = MongoClient(DB_URL)

users = client['main']['users']

def already_db(user_id):
        user = users.find_one({"user_id" : str(user_id)})
        if not user:
            return False
        return True

async def add_user(user_id, b, u):
    in_db = already_db(user_id)
    if in_db:
        return
    
    users.insert_one({"user_id": str(user_id)})
    
def remove_user(user_id):
    in_db = already_db(user_id)
    if not in_db:
        return 
    return users.delete_one({"user_id": str(user_id)})
    
def all_users():
    user = users.find({})
    usrs = len(list(user))
    return usrs

