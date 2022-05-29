import pymongo
from config import config

mongo_client = pymongo.MongoClient(config["MONGODB_URI"])

db = mongo_client.test
