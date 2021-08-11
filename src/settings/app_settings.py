import os
from dotenv import load_dotenv
from pydantic import BaseModel

class AppSettings(BaseModel):
    MONGO_CONNECTION_STRING: str
    MONGO_SPENDEE_IMPORT_COLLECTION: str
    MONGO_FINANCIAL_TRANSACTION_COLLECTION: str

def get_configuration():
    load_dotenv()

    return AppSettings(
        MONGO_CONNECTION_STRING=os.getenv("FT_MONGO_CONNECTION"),
        MONGO_SPENDEE_IMPORT_COLLECTION=os.getenv("FT_SPENDEE_IMPORT_COLLECTION"),
        MONGO_FINANCIAL_TRANSACTION_COLLECTION=os.getenv("FT_TRANSACTION_COLLECTION")
    )