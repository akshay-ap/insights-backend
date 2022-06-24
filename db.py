import pymongo
from pymongo.collection import Collection

from collection.user import User
from config import config

mongo_client = pymongo.MongoClient(config["MONGODB_URI"])

user_collection: Collection[User] = mongo_client.user_database.user
form_db = mongo_client.forms
submission_db = mongo_client.forms
reward_db = mongo_client.reward_database
