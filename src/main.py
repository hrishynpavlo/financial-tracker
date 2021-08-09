import datetime
from fastapi import FastAPI 
from rx.subject import Subject
import os
from models.monobank import MonobankTransaction, FinancialTransaction
from dotenv import load_dotenv
from pymongo import MongoClient
import json

load_dotenv()

app = FastAPI()
db = MongoClient(os.getenv("MONGO_CONNECTION")).get_default_database()
mono_sub = Subject()

@app.get("/api/version")
async def get_version():
    return { "version": "1.0.0" }

@app.post("/api/monobank/recieveTransaction")
async def recieve_monobank_transaction(monobankTransaction: MonobankTransaction):
    mono_sub.on_next(monobankTransaction)
    return { "status": "recieved" }

mono_sub.subscribe(on_next=lambda transaction: on_message(transaction))

def on_message(monobankTransaction: MonobankTransaction):
    transaction = map(monobankTransaction)
    bson = json.loads(transaction.json())
    db["test-13"].insert_one(bson)

def map(monobankTransaction: MonobankTransaction):
    transaction = FinancialTransaction( amount=abs(monobankTransaction.data.statementItem.amount) / 100, 
        title=monobankTransaction.data.statementItem.description, 
        date=datetime.datetime.utcfromtimestamp(monobankTransaction.data.statementItem.time),
        comments=monobankTransaction.data.statementItem.comment )
    return transaction

