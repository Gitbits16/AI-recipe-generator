from pymongo import MongoClient
from config import Config

client = MongoClient(Config.MONGO_URI)

db = client["recipe_ai"]

users_collection = db["users"]
recipes_collection = db["recipes"]
