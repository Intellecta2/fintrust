from sqlalchemy import Column, String, Integer, Float, DateTime, Enum
from sqlalchemy.sql import func
from app.core.database import Base
import enum
from datetime import datetime

class EmploymentTypeEnum(str, enum.Enum):
    SALARIED = "salaried"
    GOVERNMENT = "government"
    BUSINESS = "business"
    SELF_EMPLOYED = "self_employed"
    FREELANCER = "freelancer"
    UNEMPLOYED = "unemployed"

class BorrowerProfile(Base):
    __tablename__ = "borrower_profiles"
    
    id = Column(String(36), primary_key=True, index=True)
    full_name = Column(String(255), nullable=False, index=True)
    occupation = Column(String(255), nullable=True)
    employment_type = Column(Enum(EmploymentTypeEnum), nullable=False, default=EmploymentTypeEnum.SALARIED)
    
    # Financial Data
    annual_income = Column(Float, nullable=False)  # INR
    monthly_expenses = Column(Float, nullable=False)  # INR
    upi_transactions_per_month = Column(Integer, nullable=True, default=0)
    payment_history_score = Column(Float, nullable=True, default=0)  # 0-100
    savings_behavior_score = Column(Float, nullable=True, default=5)  # 1-10
    
    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    is_active = Column(Integer, default=1, index=True)
    
    def __repr__(self):
        return f"<BorrowerProfile(id={self.id}, name={self.full_name}, income={self.annual_income})>"
