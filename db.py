import pymongo
from config import config

mongo_client = pymongo.MongoClient(config["MONGODB_URI"])

user_db = mongo_client.user_database
form_db = mongo_client.form_database
submission_db = mongo_client.submissions
reward_db = mongo_client.reward_database
