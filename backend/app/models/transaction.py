from sqlalchemy import Column, String, Float, DateTime, Enum, ForeignKey
from sqlalchemy.sql import func
from app.core.database import Base
import enum

class TransactionTypeEnum(str, enum.Enum):
    CREDIT = "credit"
    DEBIT = "debit"
    TRANSFER = "transfer"
    INVESTMENT = "investment"

class Transaction(Base):
    __tablename__ = "transactions"
    
    id = Column(String(36), primary_key=True, index=True)
    borrower_id = Column(String(36), ForeignKey("borrower_profiles.id"), nullable=False, index=True)
    
    transaction_type = Column(Enum(TransactionTypeEnum), nullable=False)
    amount = Column(Float, nullable=False)  # INR
    description = Column(String(255), nullable=True)
    
    transaction_date = Column(DateTime(timezone=True), nullable=False, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    def __repr__(self):
        return f"<Transaction(id={self.id}, amount={self.amount}, type={self.transaction_type})>"
