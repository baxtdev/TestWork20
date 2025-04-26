from sqlalchemy import Column, Integer, String, DateTime, Enum,Float,TIMESTAMP
from sqlalchemy.orm import declarative_base
from sqlalchemy.sql import func

from datetime import datetime

Base = declarative_base() 

class Transaction(Base):
    __tablename__ = "transactions"
    
    transaction_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True, nullable=False)
    amount = Column(Float,index=True,nullable=False)
    currency = Column(String,index=True,nullable=False)
    timestamp = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
