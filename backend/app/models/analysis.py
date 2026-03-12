from sqlalchemy import Column, String, Integer, Float, DateTime, Boolean, Text, Enum, ForeignKey, JSON
from sqlalchemy.sql import func
from app.core.database import Base
import enum

class RiskLevelEnum(str, enum.Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"

class LoanStatusEnum(str, enum.Enum):
    APPROVED = "approved"
    REJECTED = "rejected"
    CONDITIONALLY_APPROVED = "conditionally_approved"

class CreditAnalysis(Base):
    __tablename__ = "credit_analyses"
    
    id = Column(String(36), primary_key=True, index=True)
    borrower_id = Column(String(36), ForeignKey("borrower_profiles.id"), nullable=False, index=True)
    
    # AI Predictions
    credit_score = Column(Integer, nullable=False, index=True)  # 300-900
    risk_level = Column(Enum(RiskLevelEnum), nullable=False, index=True)
    default_probability = Column(Float, nullable=False)  # 0-100 (%)
    fraud_score = Column(Float, nullable=False)  # 0-100
    is_flagged = Column(Boolean, default=False, index=True)
    
    # Loan Recommendation
    loan_approved = Column(Boolean, nullable=False, index=True)
    recommended_loan_amount = Column(Float, nullable=True)  # INR
    interest_rate = Column(Float, nullable=True)  # Percentage
    interest_band = Column(String(50), nullable=True)  # e.g., "Band A", "Band B"
    loan_category = Column(String(100), nullable=True)
    
    # Explainability
    shap_values = Column(JSON, nullable=True)
    explanation = Column(Text, nullable=True)
    improvement_tips = Column(JSON, nullable=True)
    
    # Input Data (for audit trail)
    input_data = Column(JSON, nullable=True)
    
    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    def __repr__(self):
        return f"<CreditAnalysis(id={self.id}, score={self.credit_score}, risk={self.risk_level})>"
