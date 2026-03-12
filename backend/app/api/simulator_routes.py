from fastapi import APIRouter, HTTPException, status
from app.schemas import InstantAnalysisRequest, InstantAnalysisResponse, ShapValue
from app.ml.engine import ml_engine

router = APIRouter(prefix="/v1/simulator", tags=["Simulator"])

@router.post("/credit-score-simulator", response_model=InstantAnalysisResponse)
async def credit_score_simulator(request: InstantAnalysisRequest):
    """
    What-if simulator: Test different financial scenarios
    and see how they affect credit score and loan eligibility
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

@router.post("/fraud-detection-simulator", response_model=dict)
async def fraud_detection_simulator(request: InstantAnalysisRequest):
    """
    Fraud detection simulator: Analyze transaction patterns
    for suspicious activity indicators
    """
    
    import numpy as np
    
    # Prepare features
    features = np.array([[
        request.annual_income,
        request.monthly_expenses,
        request.upi_transactions_per_month or 0,
        request.payment_history_score or 0,
        request.savings_behavior_score or 5,
        {'salaried': 100, 'government': 125, 'business': 90, 
         'self_employed': 70, 'freelancer': 55, 'unemployed': 0
        }.get(request.employment_type.value, 50)
    ]])[0]
    
    # Get fraud detection
    is_anomaly, fraud_score = ml_engine.fraud_model.detect_anomalies(features)
    
    return {
        "fraud_score": fraud_score,
        "is_flagged": is_anomaly,
        "risk_level": "High Risk" if is_anomaly else "Normal",
        "message": "Suspicious activity detected" if is_anomaly else "Activity appears normal",
        "recommendation": "Manual review recommended" if is_anomaly else "Proceed with normal processing"
    }

@router.post("/loan-eligibility-simulator", response_model=dict)
async def loan_eligibility_simulator(request: InstantAnalysisRequest):
    """
    Loan eligibility simulator: Quick check for loan approval
    and recommended loan terms
    """
    
    # Prepare data
    data = {
        'annual_income': request.annual_income,
        'monthly_expenses': request.monthly_expenses,
        'upi_transactions_per_month': request.upi_transactions_per_month or 0,
        'payment_history_score': request.payment_history_score or 0,
        'savings_behavior_score': request.savings_behavior_score or 5,
        'employment_type': request.employment_type.value
    }
    
    # Get credit score
    credit_score = ml_engine.credit_model.predict(data)
    
    # Get loan recommendation
    loan_rec = ml_engine._get_loan_recommendation(credit_score, request.annual_income)
    
    return {
        "credit_score": credit_score,
        "eligible_for_loan": loan_rec['approved'],
        "max_loan_amount": loan_rec['amount'],
        "annual_interest_rate": loan_rec['rate'],
        "interest_band": loan_rec['band'],
        "loan_category": loan_rec['category'],
        "notes": "You are eligible for a loan" if loan_rec['approved'] else "Unfortunately, you are not currently eligible for a loan"
    }
