from sqlalchemy import Column, String, Float, DateTime, Boolean, ForeignKey
from sqlalchemy.sql import func
from app.core.database import Base

class PaymentHistory(Base):
    __tablename__ = "payment_histories"
    
    id = Column(String(36), primary_key=True, index=True)
    borrower_id = Column(String(36), ForeignKey("borrower_profiles.id"), nullable=False, index=True)
    
    bill_type = Column(String(100), nullable=False)  # e.g., "electricity", "water", "internet"
    due_date = Column(DateTime(timezone=True), nullable=False)
    payment_date = Column(DateTime(timezone=True), nullable=True)
    amount = Column(Float, nullable=False)
    
    is_paid = Column(Boolean, default=False)
    days_late = Column(Float, default=0)  # Negative if paid early, positive if late
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    def __repr__(self):
        return f"<PaymentHistory(id={self.id}, bill={self.bill_type}, paid={self.is_paid})>"
