import datetime
from io import StringIO
from typing import Optional
from fastapi import FastAPI, Header, UploadFile
from fastapi.param_functions import File
from rx.subject import Subject
import os
from models.monobank import MonobankTransaction, FinancialTransaction
from dotenv import load_dotenv
from pymongo import MongoClient
import json
import csv
from io import StringIO

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

@app.post("/api/import")
async def import_csv(app: Optional[str] = "Spendee",
    telegram_user_id: int = Header(0, alias="X-TELEGRAM-USER-ID", gt=0),
    file: UploadFile = File(...)
):
    file_bytes = await file.read()
    decoded = file_bytes.decode()
    content = StringIO(decoded, newline="\n")
    csv_data = csv.DictReader(content, delimiter=",")

    records = []

    for row in csv_data:
        record = FinancialTransaction(date=datetime.datetime.strptime(row["Date"], "%Y-%m-%dT%H:%M:%S+00:00"),
            amount=abs( float(row["Amount"])), comments=row["Note"], title=row["Category name"])
        records.append(json.loads(record.json()))
   
    db["tes111"].insert_many(records)

    return { "app": app, "telegram_user_id": telegram_user_id }

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
