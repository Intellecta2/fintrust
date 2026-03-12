from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.models.borrower import BorrowerProfile, EmploymentTypeEnum
from app.schemas import (
    BorrowerProfileCreate, BorrowerProfileUpdate, BorrowerProfileResponse,
    CreditAnalysisRequest, CreditAnalysisResponse, InstantAnalysisRequest,
    InstantAnalysisResponse, ShapValue
)
from app.models.analysis import CreditAnalysis, RiskLevelEnum
from app.ml.engine import ml_engine
from datetime import datetime
import json
import uuid

router = APIRouter(prefix="/v1", tags=["Analysis"])

@router.post("/analyze/instant", response_model=InstantAnalysisResponse)
async def instant_analysis(
    request: InstantAnalysisRequest,
    db: Session = Depends(get_db)
):
    """
    Perform instant credit analysis without saving borrower profile.
    Useful for quick assessments and simulations.
    """
    
    # Prepare data for ML engine
    data = {
        'annual_income': request.annual_income,
        'monthly_expenses': request.monthly_expenses,
        'upi_transactions_per_month': request.upi_transactions_per_month or 0,
        'payment_history_score': request.payment_history_score or 0,
        'savings_behavior_score': request.savings_behavior_score or 5,
        'employment_type': request.employment_type.value
    }
    
    # Run ML analysis
    analysis_result = ml_engine.analyze_borrower(data)
    
    # Convert SHAP values to schema format
    shap_values = [ShapValue(**sv) for sv in analysis_result['shap_values']]
    
    return InstantAnalysisResponse(
        credit_score=analysis_result['credit_score'],
        risk_level=analysis_result['risk_level'],
        default_probability=analysis_result['default_probability']['high_risk'],
        fraud_score=analysis_result['fraud_score'],
        is_flagged=analysis_result['is_flagged'],
        loan_approved=analysis_result['loan_approved'],
        recommended_loan_amount=analysis_result['recommended_loan_amount'],
        interest_rate=analysis_result['interest_rate'],
        interest_band=analysis_result['interest_band'],
        loan_category=analysis_result['loan_category'],
        shap_values=shap_values,
        explanation=analysis_result['explanation'],
        improvement_tips=analysis_result['improvement_tips']
    )

@router.post("/borrowers", response_model=BorrowerProfileResponse)
async def create_borrower(
    request: BorrowerProfileCreate,
    db: Session = Depends(get_db)
):
    """Create a new borrower profile"""
    
    # Check if borrower already exists
    existing = db.query(BorrowerProfile).filter(
        BorrowerProfile.full_name.ilike(request.full_name)
    ).first()
    
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Borrower with name {request.full_name} already exists"
        )
    
    # Create new borrower
    db_borrower = BorrowerProfile(
        id=str(uuid.uuid4()),
        full_name=request.full_name,
        occupation=request.occupation,
        employment_type=EmploymentTypeEnum(request.employment_type.value),
        annual_income=request.annual_income,
        monthly_expenses=request.monthly_expenses,
        upi_transactions_per_month=request.upi_transactions_per_month or 0,
        payment_history_score=request.payment_history_score or 0,
        savings_behavior_score=request.savings_behavior_score or 5,
        is_active=True
    )
    
    db.add(db_borrower)
    db.commit()
    db.refresh(db_borrower)
    
    return BorrowerProfileResponse.model_validate(db_borrower)

@router.get("/borrowers/{borrower_id}", response_model=BorrowerProfileResponse)
async def get_borrower(
    borrower_id: str,
    db: Session = Depends(get_db)
):
    """Get borrower profile by ID"""
    
    borrower = db.query(BorrowerProfile).filter(
        BorrowerProfile.id == borrower_id,
        BorrowerProfile.is_active == True
    ).first()
    
    if not borrower:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Borrower not found"
        )
    
    return BorrowerProfileResponse.model_validate(borrower)

@router.get("/borrowers", response_model=List[BorrowerProfileResponse])
async def list_borrowers(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """List all active borrowers"""
    
    borrowers = db.query(BorrowerProfile).filter(
        BorrowerProfile.is_active == True
    ).offset(skip).limit(limit).all()
    
    return [BorrowerProfileResponse.model_validate(b) for b in borrowers]

@router.put("/borrowers/{borrower_id}", response_model=BorrowerProfileResponse)
async def update_borrower(
    borrower_id: str,
    request: BorrowerProfileUpdate,
    db: Session = Depends(get_db)
):
    """Update borrower profile"""
    
    borrower = db.query(BorrowerProfile).filter(
        BorrowerProfile.id == borrower_id,
        BorrowerProfile.is_active == True
    ).first()
    
    if not borrower:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Borrower not found"
        )
    
    # Update fields
    update_data = request.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        if field == 'employment_type':
            setattr(borrower, field, EmploymentTypeEnum(value.value))
        else:
            setattr(borrower, field, value)
    
    borrower.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(borrower)
    
    return BorrowerProfileResponse.model_validate(borrower)

@router.post("/analyze/{borrower_id}", response_model=CreditAnalysisResponse)
async def analyze_borrower(
    borrower_id: str,
    db: Session = Depends(get_db)
):
    """Analyze borrower and generate credit assessment"""
    
    # Get borrower
    borrower = db.query(BorrowerProfile).filter(
        BorrowerProfile.id == borrower_id,
        BorrowerProfile.is_active == True
    ).first()
    
    if not borrower:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Borrower not found"
        )
    
    # Check if recent analysis exists (within 24 hours)
    recent_analysis = db.query(CreditAnalysis).filter(
        CreditAnalysis.borrower_id == borrower_id
    ).order_by(CreditAnalysis.created_at.desc()).first()
    
    if recent_analysis:
        # Reuse recent analysis (avoid redundant ML calls)
        return CreditAnalysisResponse.model_validate(recent_analysis)
    
    # Prepare data for ML engine
    data = {
        'annual_income': borrower.annual_income,
        'monthly_expenses': borrower.monthly_expenses,
        'upi_transactions_per_month': borrower.upi_transactions_per_month,
        'payment_history_score': borrower.payment_history_score,
        'savings_behavior_score': borrower.savings_behavior_score,
        'employment_type': borrower.employment_type.value
    }
    
    # Run ML analysis
    analysis_result = ml_engine.analyze_borrower(data)
    
    # Save to database
    db_analysis = CreditAnalysis(
        id=str(uuid.uuid4()),
        borrower_id=borrower_id,
        credit_score=analysis_result['credit_score'],
        risk_level=RiskLevelEnum(analysis_result['risk_level']),
        default_probability=analysis_result['default_probability']['high_risk'],
        fraud_score=analysis_result['fraud_score'],
        is_flagged=analysis_result['is_flagged'],
        loan_approved=analysis_result['loan_approved'],
        recommended_loan_amount=analysis_result['recommended_loan_amount'],
        interest_rate=analysis_result['interest_rate'],
        interest_band=analysis_result['interest_band'],
        loan_category=analysis_result['loan_category'],
        shap_values=json.dumps([{
            'feature': sv['feature'],
            'contribution': sv['contribution'],
            'direction': sv['direction'],
            'description': sv['description']
        } for sv in analysis_result['shap_values']]),
        explanation=analysis_result['explanation'],
        improvement_tips=json.dumps(analysis_result['improvement_tips']),
        input_data=json.dumps(data)
    )
    
    db.add(db_analysis)
    db.commit()
    db.refresh(db_analysis)
    
    return CreditAnalysisResponse.model_validate(db_analysis)

@router.get("/analyze/{borrower_id}", response_model=CreditAnalysisResponse)
async def get_latest_analysis(
    borrower_id: str,
    db: Session = Depends(get_db)
):
    """Get latest credit analysis for borrower"""
    
    analysis = db.query(CreditAnalysis).filter(
        CreditAnalysis.borrower_id == borrower_id
    ).order_by(CreditAnalysis.created_at.desc()).first()
    
    if not analysis:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No analysis found for this borrower"
        )
    
    return CreditAnalysisResponse.model_validate(analysis)

@router.get("/portfolio/statistics")
async def get_portfolio_stats(db: Session = Depends(get_db)):
    """Get portfolio statistics and analytics"""
    
    total_borrowers = db.query(BorrowerProfile).filter(
        BorrowerProfile.is_active == True
    ).count()
    
    analyses = db.query(CreditAnalysis).all()
    
    if not analyses:
        return {
            "total_borrowers": total_borrowers,
            "avg_credit_score": 0,
            "approval_rate": 0,
            "fraud_alerts_count": 0,
            "avg_fraud_score": 0,
            "portfolio_risk_distribution": {
                "Low": 0,
                "Medium": 0,
                "High": 0
            }
        }
    
    credit_scores = [a.credit_score for a in analyses]
    approved = sum(1 for a in analyses if a.loan_approved)
    fraud_alerts = sum(1 for a in analyses if a.is_flagged)
    fraud_scores = [a.fraud_score for a in analyses]
    
    risk_dist = {
        "Low": sum(1 for a in analyses if a.risk_level == RiskLevelEnum.LOW),
        "Medium": sum(1 for a in analyses if a.risk_level == RiskLevelEnum.MEDIUM),
        "High": sum(1 for a in analyses if a.risk_level == RiskLevelEnum.HIGH)
    }
    
    return {
        "total_borrowers": total_borrowers,
        "avg_credit_score": sum(credit_scores) / len(credit_scores) if credit_scores else 0,
        "approval_rate": (approved / len(analyses)) * 100 if analyses else 0,
        "fraud_alerts_count": fraud_alerts,
        "avg_fraud_score": sum(fraud_scores) / len(fraud_scores) if fraud_scores else 0,
        "portfolio_risk_distribution": risk_dist
    }

@router.delete("/borrowers/{borrower_id}")
async def delete_borrower(
    borrower_id: str,
    db: Session = Depends(get_db)
):
    """Soft delete borrower profile"""
    
    borrower = db.query(BorrowerProfile).filter(
        BorrowerProfile.id == borrower_id
    ).first()
    
    if not borrower:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Borrower not found"
        )
    
    borrower.is_active = False
    borrower.updated_at = datetime.utcnow()
    db.commit()
    
    return {"message": f"Borrower {borrower_id} deleted successfully"}
