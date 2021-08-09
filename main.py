import datetime
from fastapi import FastAPI 
from rx.subject import Subject
from models.monobank import MonobankTransaction, FinancialTransaction

app = FastAPI()

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
    print(transaction)

def map(monobankTransaction: MonobankTransaction):
    transaction = FinancialTransaction( amount=abs(monobankTransaction.data.statementItem.amount) / 100, 
        title=monobankTransaction.data.statementItem.description, 
        date=datetime.datetime.utcfromtimestamp(monobankTransaction.data.statementItem.time),
        comments=monobankTransaction.data.statementItem.comment )
    return transaction