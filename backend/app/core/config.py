from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    # API
    environment: str = "development"
    debug: bool = True
    api_title: str = "FinTrust AI"
    api_version: str = "1.0.0"
    api_description: str = "Advanced AI-powered credit scoring and risk assessment"
    
    # Database
    database_url: str = "postgresql://user:password@localhost:5432/fintrust_ai_db"
    
    # CORS
    allowed_origins: List[str] = [
        "http://localhost:3000",
        "http://localhost:5173",
        "http://127.0.0.1:3000"
    ]
    
    # JWT
    secret_key: str = "your-secret-key-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 1440
    
    # ML Models
    model_credit_score_path: str = "./models/credit_score_xgboost.pkl"
    model_fraud_path: str = "./models/fraud_detection_isolationforest.pkl"
    model_default_risk_path: str = "./models/default_risk_randomforest.pkl"
    
    # Redis
    redis_url: str = "redis://localhost:6379/0"
    
    class Config:
        env_file = ".env"
        case_sensitive = False

settings = Settings()
