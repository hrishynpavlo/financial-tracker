from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class StatementItem(BaseModel):
    time: int
    description: str
    mcc: int
    hold: bool
    amount: int
    operationAmount: int
    currencyCode: int
    commissionRate: int
    cashbackAmount: int
    balance: int
    comment: Optional[str]
    receiptId: str
    counterEdrpou: Optional[str]
    counterIban: Optional[str]

class TransactionData(BaseModel):
    account: str
    statementItem: StatementItem

class MonobankTransaction(BaseModel): 
    type: str
    data: TransactionData

class FinancialTransaction(BaseModel): 
    amount: float
    date: datetime
    category: str = "Other"
    title: str
    comments: Optional[str]
