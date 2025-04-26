from fastapi import APIRouter,Depends,HTTPException

from sqlalchemy.exc import IntegrityError
from sqlalchemy import select

from typing import List

from .db import engine,get_db,AsyncSession
from .models import Base,Transaction
from .schemas import TransactionBase,TransactionResponse
from .utils import calculate_transaction_statistics
from .tasks import update_statistics_task
from .conf import redis_client
from .services import create_transaction,list_transactions,delete_transactions

router = APIRouter()


@router.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@router.post("/transactions/", response_model=TransactionResponse)
async def transactions_post(transaction: TransactionBase, db: AsyncSession = Depends(get_db)):
    try:
        new_transaction = await create_transaction(transaction,db)
        
    except IntegrityError as e:
        await db.rollback()
        raise HTTPException(
            status_code=400,
            detail="Transaction with this ID already exists."
        )
    task = update_statistics_task.delay()
    return TransactionResponse(
        task_id=task.id,
        message="Transaction received"
    )


@router.get('/transactions/',response_model=List[TransactionBase])
async def get_transacctions(db: AsyncSession = Depends(get_db)):
    transactions = await list_transactions(db)
    return transactions


@router.delete("/transactions/")
async def transactions_delete(db: AsyncSession = Depends(get_db)):
    result = await delete_transactions(db)
    if result:
        redis_client.delete('statistics')
        return {"detail": "All transactions deleted"}
    
    raise HTTPException(
            status_code=400,
            detail="Error deleting data"
        )


@router.get("/statistics/")
async def get_statistics(db: AsyncSession = Depends(get_db)):
    cached_stats = redis_client.get("statistics")

    if cached_stats:
        return eval(cached_stats) 
    
    result = await db.execute(select(Transaction.transaction_id, Transaction.amount))
    transactions = result.all()
    print(transactions)
    stats = calculate_transaction_statistics(transactions)

    redis_client.setex("statistics", 3600, str(stats))

    return stats