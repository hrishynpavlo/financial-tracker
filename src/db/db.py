from settings.app_settings import AppSettings
from pymongo import MongoClient
import json

def get_db(configuration: AppSettings):
    client = MongoClient(configuration.MONGO_CONNECTION_STRING).get_default_database()
    if configuration.MONGO_FINANCIAL_CATEGORY_COLLECTION not in client.list_collection_names():
        with open('seed.json', encoding="utf-8") as seed_json:
            seed = json.load(seed_json)
            client[configuration.MONGO_FINANCIAL_CATEGORY_COLLECTION].insert_many(seed["categories"])

            
    return client