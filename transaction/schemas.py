from pydantic import BaseModel

from datetime import datetime


class TransactionBase(BaseModel):
    transaction_id : int
    user_id : int
    amount : float
    currency : str
    timestamp : datetime


class TransactionResponse(BaseModel):
    task_id : str
    message : str