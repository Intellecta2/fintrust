import pickle
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier, IsolationForest
from xgboost import XGBRegressor
import shap
from typing import Dict, List, Tuple
import os
from pathlib import Path

class CreditScoreModel:
    """XGBoost model for credit score prediction (300-900)"""
    
    def __init__(self):
        self.model = None
        self.scaler = StandardScaler()
        self.feature_names = [
            'annual_income', 'monthly_expenses', 'upi_transactions',
            'payment_history', 'savings_behavior', 'employment_score'
        ]
        
    def train(self, X: np.ndarray, y: np.ndarray):
        """Train the credit score model"""
        X_scaled = self.scaler.fit_transform(X)
        self.model = XGBRegressor(
            n_estimators=100,
            max_depth=6,
            learning_rate=0.1,
            random_state=42,
            objective='reg:squarederror'
        )
        self.model.fit(X_scaled, y)
        return self
    
    def predict(self, data: Dict) -> int:
        """Predict credit score (300-900)"""
        features = self._prepare_features(data)
        features_scaled = self.scaler.transform([features])
        score = self.model.predict(features_scaled)[0]
        # Clamp between 300 and 900
        return max(300, min(900, int(score)))
    
    def get_feature_importance(self, data: Dict) -> List[Dict]:
        """Get SHAP values for explainability"""
        features = self._prepare_features(data)
        features_scaled = self.scaler.transform([features])
        
        # Create explainer
        explainer = shap.TreeExplainer(self.model)
        shap_values = explainer.shap_values(features_scaled)
        
        # Format output
        importance = []
        for i, feature in enumerate(self.feature_names):
            importance.append({
                "feature": feature,
                "contribution": float(shap_values[0][i]),
                "direction": "positive" if shap_values[0][i] > 0 else "negative",
                "description": f"Impact of {feature} on score"
            })
        
        return sorted(importance, key=lambda x: abs(x["contribution"]), reverse=True)
    
    def _prepare_features(self, data: Dict) -> List[float]:
        """Convert input data to feature vector"""
        employment_scores = {
            'salaried': 100,
            'government': 125,
            'business': 90,
            'self_employed': 70,
            'freelancer': 55,
            'unemployed': 0
        }
        
        return [
            data.get('annual_income', 0),
            data.get('monthly_expenses', 0),
            data.get('upi_transactions_per_month', 0),
            data.get('payment_history_score', 0),
            data.get('savings_behavior_score', 5),
            employment_scores.get(data.get('employment_type', 'salaried'), 50)
        ]
    
    def save(self, path: str):
        """Save model to disk"""
        with open(path, 'wb') as f:
            pickle.dump({'model': self.model, 'scaler': self.scaler}, f)
    
    def load(self, path: str):
        """Load model from disk"""
        if os.path.exists(path):
            with open(path, 'rb') as f:
                data = pickle.load(f)
                self.model = data['model']
                self.scaler = data['scaler']
        return self

class DefaultRiskModel:
    """Random Forest model for default risk prediction"""
    
    def __init__(self):
        self.model = None
        self.scaler = StandardScaler()
        
    def train(self, X: np.ndarray, y: np.ndarray):
        """Train the default risk model"""
        X_scaled = self.scaler.fit_transform(X)
        self.model = RandomForestClassifier(
            n_estimators=100,
            max_depth=10,
            random_state=42,
            class_weight='balanced'
        )
        self.model.fit(X_scaled, y)
        return self
    
    def predict_probability(self, features: np.ndarray) -> Dict[str, float]:
        """Predict probability of default"""
        features_scaled = self.scaler.transform([features])
        probabilities = self.model.predict_proba(features_scaled)[0]
        
        return {
            'low_risk': float(probabilities[0]),
            'medium_risk': float(probabilities[1] if len(probabilities) > 1 else 0),
            'high_risk': float(probabilities[2] if len(probabilities) > 2 else 0)
        }

class FraudDetectionModel:
    """Isolation Forest for anomaly detection"""
    
    def __init__(self):
        self.model = None
        self.scaler = StandardScaler()
        
    def train(self, X: np.ndarray):
        """Train the fraud detection model"""
        X_scaled = self.scaler.fit_transform(X)
        self.model = IsolationForest(
            contamination=0.1,
            random_state=42,
            n_estimators=100
        )
        self.model.fit(X_scaled)
        return self
    
    def predict_fraud_score(self, features: np.ndarray) -> float:
        """
        Predict fraud score (0-100)
        Higher score = more likely to be fraud
        """
        features_scaled = self.scaler.transform([features])
        
        # Get anomaly score (-1 for anomalies, 1 for normal)
        anomaly_score = self.model.score_samples(features_scaled)[0]
        
        # Convert to 0-100 scale
        # anomaly_score ranges from -infinity to 0.3 typically
        # Normalize to 0-100
        fraud_score = max(0, min(100, (1 - (anomaly_score + 0.5)) * 50))
        
        return float(fraud_score)
    
    def detect_anomalies(self, features: np.ndarray) -> Tuple[bool, float]:
        """
        Detect if features are anomalous
        Returns (is_anomaly, fraud_score)
        """
        fraud_score = self.predict_fraud_score(features)
        is_anomaly = fraud_score > 60  # Threshold for flagging
        return is_anomaly, fraud_score

class MLEngine:
    """Main ML engine coordinating all models"""
    
    def __init__(self):
        self.credit_model = CreditScoreModel()
        self.default_model = DefaultRiskModel()
        self.fraud_model = FraudDetectionModel()
        self.loaded = False
    
    def initialize(self):
        """Initialize models (create dummy if not exist)"""
        # For demo purposes, we'll create simple trained models
        # In production, these would be trained on real data
        
        # Create dummy training data
        X_credit = np.random.randn(100, 6) * 100000
        y_credit = np.random.randint(300, 900, 100)
        
        X_fraud = np.random.randn(100, 6) * 100000
        
        # Train models
        self.credit_model.train(X_credit, y_credit)
        self.fraud_model.train(X_fraud)
        
        self.loaded = True
    
    def analyze_borrower(self, borrower_data: Dict) -> Dict:
        """Comprehensive borrower analysis"""
        
        # Prepare features
        features = self._prepare_features(borrower_data)
        
        # Get credit score
        credit_score = self.credit_model.predict(borrower_data)
        
        # Get risk level and default probability
        risk_probs = self.default_model.predict_probability(features)
        risk_level = self._determine_risk_level(credit_score)
        
        # Get fraud score
        is_fraud, fraud_score = self.fraud_model.detect_anomalies(features)
        
        # Get loan recommendation
        loan_rec = self._get_loan_recommendation(credit_score, borrower_data.get('annual_income', 0))
        
        # Get SHAP values
        shap_values = self.credit_model.get_feature_importance(borrower_data)
        
        # Generate explanation
        explanation = self._generate_explanation(credit_score, risk_level, borrower_data)
        
        # Generate improvement tips
        improvement_tips = self._generate_improvement_tips(shap_values, credit_score)
        
        return {
            'credit_score': credit_score,
            'risk_level': risk_level,
            'default_probability': risk_probs,
            'fraud_score': fraud_score,
            'is_flagged': is_fraud,
            'loan_approved': loan_rec['approved'],
            'recommended_loan_amount': loan_rec['amount'],
            'interest_rate': loan_rec['rate'],
            'interest_band': loan_rec['band'],
            'loan_category': loan_rec['category'],
            'shap_values': shap_values,
            'explanation': explanation,
            'improvement_tips': improvement_tips
        }
    
    def _prepare_features(self, data: Dict) -> np.ndarray:
        """Prepare features for ML models"""
        employment_scores = {
            'salaried': 100,
            'government': 125,
            'business': 90,
            'self_employed': 70,
            'freelancer': 55,
            'unemployed': 0
        }
        
        return np.array([[
            data.get('annual_income', 0),
            data.get('monthly_expenses', 0),
            data.get('upi_transactions_per_month', 0),
            data.get('payment_history_score', 0),
            data.get('savings_behavior_score', 5),
            employment_scores.get(data.get('employment_type', 'salaried'), 50)
        ]])[0]
    
    def _determine_risk_level(self, score: int) -> str:
        """Determine risk level from credit score"""
        if score >= 750:
            return "Low"
        elif score >= 600:
            return "Medium"
        else:
            return "High"
    
    def _get_loan_recommendation(self, score: int, income: float) -> Dict:
        """Get loan recommendation based on score"""
        monthly_income = income / 12
        
        tiers = [
            {'min': 800, 'mult': 60, 'rate': 7.2, 'cat': 'Premium Elite', 'band': 'Band A'},
            {'min': 750, 'mult': 48, 'rate': 9.5, 'cat': 'Prime', 'band': 'Band B'},
            {'min': 700, 'mult': 36, 'rate': 11.5, 'cat': 'Standard', 'band': 'Band C'},
            {'min': 650, 'mult': 24, 'rate': 13.5, 'cat': 'Subprime', 'band': 'Band D'},
            {'min': 600, 'mult': 12, 'rate': 16.0, 'cat': 'High Risk', 'band': 'Band E'},
        ]
        
        for tier in tiers:
            if score >= tier['min']:
                return {
                    'approved': True,
                    'amount': max(100000, int(monthly_income * tier['mult'])),
                    'rate': tier['rate'],
                    'band': tier['band'],
                    'category': tier['cat']
                }
        
        return {
            'approved': False,
            'amount': 0,
            'rate': 0,
            'band': 'N/A',
            'category': 'Not Eligible'
        }
    
    def _generate_explanation(self, score: int, risk_level: str, data: Dict) -> str:
        """Generate AI explanation"""
        explanations = {
            'Low': f"Excellent credit profile. With a score of {score}, you demonstrate strong financial stability and reliable payment history.",
            'Medium': f"Fair credit profile. Your score of {score} indicates moderate financial health. Focus on improving payment consistency.",
            'High': f"Needs improvement. Your score of {score} suggests financial risk. Consider increasing savings and reducing expenses."
        }
        return explanations.get(risk_level, "Analysis complete.")
    
    def _generate_improvement_tips(self, shap_values: List[Dict], score: int) -> List[str]:
        """Generate improvement tips"""
        tips = []
        
        # Find negative factors
        negative_factors = [s for s in shap_values if s['direction'] == 'negative']
        negative_factors = sorted(negative_factors, key=lambda x: abs(x['contribution']), reverse=True)
        
        for factor in negative_factors[:3]:
            if 'expense' in factor['feature'].lower():
                tips.append("Reduce monthly expenses by 10-15% to improve your score")
            elif 'payment' in factor['feature'].lower():
                tips.append("Maintain consistent on-time payments for utilities and bills")
            elif 'upi' in factor['feature'].lower():
                tips.append("Increase digital transaction frequency to build financial footprint")
            elif 'saving' in factor['feature'].lower():
                tips.append("Build emergency fund with regular savings (aim for 6 months expenses)")
        
        if score < 600:
            tips.append("Consider secured loan options while building credit")
        
        if len(tips) < 3:
            tips.append("Maintain consistent income and regular financial discipline")
        
        return tips[:3]

# Global ML engine instance
ml_engine = MLEngine()
