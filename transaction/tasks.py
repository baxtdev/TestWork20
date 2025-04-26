import redis

from sqlalchemy import select

from celery import Celery

from .utils import calculate_transaction_statistics,Transaction
from .db import sync_get_db
from . import conf  

redis_client = conf.redis_client

celery_app = Celery('tasks', broker=conf.REDIS_BROKER_URL)

@celery_app.task
def update_statistics_task():
    with sync_get_db() as db:
        result = db.execute(select(Transaction.transaction_id, Transaction.amount))
        transactions = result.all()

    stats = calculate_transaction_statistics(transactions)
    redis_client.setex("statistics", 3600, str(stats))

    return stats