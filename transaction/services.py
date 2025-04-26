from .models import Transaction
from sqlalchemy import delete,select

async def create_transaction(data,db):
    new_transaction = Transaction(**data.dict())
    db.add(new_transaction)
    await db.commit()
    await db.refresh(new_transaction)
    return new_transaction

async def delete_transactions(db):
    await db.execute(delete(Transaction))
    await db.commit()
    return True

async def list_transactions(db):
    result = await db.execute(select(Transaction))
    transactions = result.scalars().all()
    return transactions