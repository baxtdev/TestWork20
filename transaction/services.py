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

async def list_transactions(db, page: int = 1, page_size: int = 10):
    offset = (page - 1) * page_size
    
    result = await db.execute(
        select(Transaction)
        .limit(page_size)  
        .offset(offset)   
    )
    transactions = result.scalars().all()
    
    return transactions