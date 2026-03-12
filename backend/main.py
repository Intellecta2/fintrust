from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZIPMiddleware
from fastapi.responses import JSONResponse
from app.core.config import settings
from app.core.database import engine, Base
from app.models.borrower import BorrowerProfile
from app.models.analysis import CreditAnalysis
from app.models.transaction import Transaction
from app.models.payment_history import PaymentHistory
from app.api import analysis_router, simulator_router
from app.ml.engine import ml_engine
from datetime import datetime
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create all database tables
Base.metadata.create_all(bind=engine)

# Initialize ML engine
ml_engine.initialize()

# Create FastAPI app
app = FastAPI(
    title="FinTrust AI - Intelligent Fintech Platform",
    description="Advanced AI-powered credit scoring, fraud detection, and financial analytics platform",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add GZIP compression
app.add_middleware(GZIPMiddleware, minimum_size=1000)

# Include routers
app.include_router(analysis_router)
app.include_router(simulator_router)

@app.get("/", tags=["Root"])
async def root():
    """Root endpoint - returns API information"""
    return {
        "name": "FinTrust AI",
        "version": "1.0.0",
        "status": "operational",
        "timestamp": datetime.utcnow().isoformat(),
        "docs": "/api/docs",
        "redoc": "/api/redoc"
    }

@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "service": "FinTrust AI Backend",
        "version": "1.0.0"
    }

@app.get("/api/v1/health", tags=["Health"])
async def api_health():
    """API health check with database status"""
    try:
        from app.core.database import SessionLocal
        db = SessionLocal()
        # Try a simple query
        db.query(BorrowerProfile).count()
        db.close()
        db_status = "connected"
    except Exception as e:
        logger.error(f"Database connection error: {e}")
        db_status = "disconnected"
    
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "service": "FinTrust AI Backend",
        "version": "1.0.0",
        "database": db_status,
        "ml_engine": "initialized" if ml_engine.loaded else "not_initialized"
    }

@app.get("/api/v1/info", tags=["Info"])
async def api_info():
    """Get API information and available endpoints"""
    return {
        "service": "FinTrust AI",
        "version": "1.0.0",
        "description": "Intelligent Fintech Platform with AI Credit Scoring and Fraud Detection",
        "endpoints": {
            "analysis": {
                "instant_analysis": "POST /v1/analyze/instant",
                "create_borrower": "POST /v1/borrowers",
                "get_borrower": "GET /v1/borrowers/{borrower_id}",
                "list_borrowers": "GET /v1/borrowers",
                "update_borrower": "PUT /v1/borrowers/{borrower_id}",
                "analyze_borrower": "POST /v1/analyze/{borrower_id}",
                "get_analysis": "GET /v1/analyze/{borrower_id}",
                "portfolio_stats": "GET /v1/portfolio/statistics"
            },
            "simulator": {
                "credit_simulator": "POST /v1/simulator/credit-score-simulator",
                "fraud_simulator": "POST /v1/simulator/fraud-detection-simulator",
                "eligibility_simulator": "POST /v1/simulator/loan-eligibility-simulator"
            }
        },
        "features": [
            "Credit Score Prediction (300-900)",
            "Default Risk Analysis",
            "Fraud Detection with SHAP Explainability",
            "What-if Loan Simulator",
            "Portfolio Analytics",
            "Borrower Profile Management",
            "Interest Rate Recommendations",
            "Risk-based Loan Categorization"
        ]
    }

@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """Global exception handler"""
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "detail": "Internal server error",
            "error": str(exc) if settings.DEBUG else "An error occurred",
            "timestamp": datetime.utcnow().isoformat()
        }
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=settings.DEBUG,
        log_level="info"
    )
