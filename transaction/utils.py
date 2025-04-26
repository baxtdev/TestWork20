import heapq
from typing import List, Dict, Any
from .models import Transaction

def calculate_transaction_statistics(transactions: List[Dict[str, Any]]) -> Dict[str, Any]:

    total_transactions = 0
    total_amount = 0.0
    top_transactions_heap = []

    for tx in transactions:
        tx:Transaction
        tx_id = tx.transaction_id
        amount = tx.amount

        total_transactions += 1
        total_amount += amount

        if len(top_transactions_heap) < 3:
            heapq.heappush(top_transactions_heap, (amount, tx_id))
        else:
            heapq.heappushpop(top_transactions_heap, (amount, tx_id))

    top_transactions = sorted(top_transactions_heap, reverse=True)

    return {
        "total_transactions": total_transactions,
        "average_transaction_amount": round(total_amount / total_transactions, 2) if total_transactions else 0.0,
        "top_transactions": [
            {"transaction_id": str(tx_id), "amount": amount}
            for amount, tx_id in top_transactions
        ]
    }
