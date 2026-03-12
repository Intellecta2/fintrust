from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum

class EmploymentType(str, Enum):
    SALARIED = "salaried"
    GOVERNMENT = "government"
    BUSINESS = "business"
    SELF_EMPLOYED = "self_employed"
    FREELANCER = "freelancer"
    UNEMPLOYED = "unemployed"

# ===== BORROWER SCHEMAS =====
class BorrowerProfileCreate(BaseModel):
    full_name: str = Field(..., min_length=2, max_length=255)
    occupation: Optional[str] = Field(None, max_length=255)
    employment_type: EmploymentType
    annual_income: float = Field(..., gt=0)
    monthly_expenses: float = Field(..., ge=0)
    upi_transactions_per_month: Optional[int] = Field(default=0, ge=0)
    payment_history_score: Optional[float] = Field(default=0, ge=0, le=100)
    savings_behavior_score: Optional[float] = Field(default=5, ge=1, le=10)

class BorrowerProfileUpdate(BaseModel):
    full_name: Optional[str] = None
    occupation: Optional[str] = None
    employment_type: Optional[EmploymentType] = None
    annual_income: Optional[float] = None
    monthly_expenses: Optional[float] = None
    upi_transactions_per_month: Optional[int] = None
    payment_history_score: Optional[float] = None
    savings_behavior_score: Optional[float] = None

class BorrowerProfileResponse(BaseModel):
    id: str
    full_name: str
    occupation: Optional[str]
    employment_type: EmploymentType
    annual_income: float
    monthly_expenses: float
    upi_transactions_per_month: int
    payment_history_score: float
    savings_behavior_score: float
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

# ===== CREDIT ANALYSIS SCHEMAS =====
class ShapValue(BaseModel):
    feature: str
    contribution: float
    direction: str  # "positive" or "negative"
    description: str

class CreditAnalysisRequest(BaseModel):
    borrower_id: str

class CreditAnalysisResponse(BaseModel):
    id: str
    borrower_id: str
    credit_score: int
    risk_level: str
    default_probability: float
    fraud_score: float
    is_flagged: bool
    loan_approved: bool
    recommended_loan_amount: Optional[float]
    interest_rate: Optional[float]
    interest_band: Optional[str]
    loan_category: Optional[str]
    shap_values: Optional[List[ShapValue]]
    explanation: Optional[str]
    improvement_tips: Optional[List[str]]
    created_at: datetime
    
    class Config:
        from_attributes = True

# ===== INSTANT ANALYSIS SCHEMAS =====
class InstantAnalysisRequest(BaseModel):
    """For quick analysis without saving borrower profile"""
    full_name: str
    occupation: Optional[str]
    employment_type: EmploymentType
    annual_income: float
    monthly_expenses: float
    upi_transactions_per_month: Optional[int] = 0
    payment_history_score: Optional[float] = 0
    savings_behavior_score: Optional[float] = 5

class InstantAnalysisResponse(BaseModel):
    credit_score: int
    risk_level: str
    default_probability: float
    fraud_score: float
    is_flagged: bool
    loan_approved: bool
    recommended_loan_amount: float
    interest_rate: float
    interest_band: str
    loan_category: str
    shap_values: List[ShapValue]
    explanation: str
    improvement_tips: List[str]

# ===== PORTFOLIO ANALYTICS =====
class PortfolioStats(BaseModel):
    total_borrowers: int
    avg_credit_score: float
    approval_rate: float
    fraud_alerts_count: int
    avg_fraud_score: float
    portfolio_risk_distribution: dict

# ===== ERROR SCHEMAS =====
class ErrorResponse(BaseModel):
    detail: str
    error_code: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)
