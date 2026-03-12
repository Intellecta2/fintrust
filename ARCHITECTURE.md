# FinTrust AI - System Architecture

## 🏗️ High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Frontend (Next.js/React)                 │
│  Dashboard │ Analysis │ Simulator │ Portfolio │ Settings    │
│            (http://localhost:3000)                           │
└────────────────────────┬────────────────────────────────────┘
                         │ HTTP/REST
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                  API Gateway / Reverse Proxy                 │
│                     (CORS Enabled)                           │
└────────────────────────┬────────────────────────────────────┘
                         │ HTTP/REST
                         ▼
┌─────────────────────────────────────────────────────────────┐
│              FastAPI Backend (http://localhost:8000)         │
│  ┌─────────────────────────────────────────────────────────┤
│  │ Routing Layer                                            │
│  │ ├─ POST /v1/analyze/instant                             │
│  │ ├─ POST /v1/borrowers                                   │
│  │ ├─ POST /v1/analyze/{id}                                │
│  │ └─ POST /v1/simulator/*                                 │
│  └─────────────────────────────────────────────────────────┤
│  ┌─────────────────────────────────────────────────────────┤
│  │ ML Engine Layer                                          │
│  │ ├─ CreditScoreModel (XGBoost)                           │
│  │ ├─ FraudDetectionModel (Isolation Forest)               │
│  │ ├─ DefaultRiskModel (RandomForest)                      │
│  │ └─ SHAP Explainer                                       │
│  └─────────────────────────────────────────────────────────┤
│  ┌─────────────────────────────────────────────────────────┤
│  │ Service Layer (Business Logic)                           │
│  │ ├─ BorrowerService                                      │
│  │ ├─ AnalysisService                                      │
│  │ └─ SimulatorService                                     │
│  └─────────────────────────────────────────────────────────┤
│  ┌─────────────────────────────────────────────────────────┤
│  │ Data Access Layer (SQLAlchemy ORM)                       │
│  │ ├─ BorrowerProfile                                      │
│  │ ├─ CreditAnalysis                                       │
│  │ ├─ Transaction                                          │
│  │ └─ PaymentHistory                                       │
│  └─────────────────────────────────────────────────────────┤
└────────────────────────┬────────────────────────────────────┘
                         │ SQL
                         ▼
┌─────────────────────────────────────────────────────────────┐
│           PostgreSQL Database (Port 5432)                    │
│  ┌──────────────────────────────────────────────────────┐   │
│  │ Schemas:                                             │   │
│  │ ├─ borrower_profiles (1000+ records)                │   │
│  │ ├─ credit_analyses (1000+ records)                  │   │
│  │ ├─ transactions (10000+ records)                    │   │
│  │ └─ payment_history (5000+ records)                  │   │
│  │                                                      │   │
│  │ Indexes: Created on all frequently queried fields   │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

---

## 📦 Component Details

### Frontend (Next.js/React)
```
/frontend/
  ├── app/
  │   ├── page.tsx              # Home page
  │   ├── layout.tsx            # Root layout with providers
  │   ├── dashboard/
  │   │   └── page.tsx          # Portfolio dashboard
  │   ├── analysis/
  │   │   └── page.tsx          # Credit analysis form
  │   └── simulator/
  │       └── page.tsx          # What-if simulator
  ├── src/
  │   ├── contexts/
  │   │   ├── LanguageContext.tsx    # i18n support (EN/HI)
  │   │   └── ThemeContext.tsx       # Dark mode support
  │   ├── services/
  │   │   └── api.ts                 # Axios API client
  │   └── utils/                    # Helper functions
  ├── globals.css               # Global styles
  └── tailwind.config.ts        # Tailwind configuration
```

**Key Features:**
- Responsive design (mobile-first)
- Real-time data updates
- Multilingual support (English/Hindi)
- Dark mode support (prepared)
- SHAP visualization ready

---

### Backend (FastAPI)

```
/backend/
  ├── main.py              # FastAPI application entry point
  ├── requirements.txt     # Python dependencies (23 packages)
  ├── app/
  │   ├── core/
  │   │   ├── config.py              # Pydantic settings management
  │   │   └── database.py            # SQLAlchemy engine & session
  │   ├── models/
  │   │   ├── borrower.py            # BorrowerProfile ORM model
  │   │   ├── analysis.py            # CreditAnalysis ORM model
  │   │   ├── transaction.py         # Transaction ORM model
  │   │   └── payment_history.py     # PaymentHistory ORM model
  │   ├── schemas/
  │   │   └── __init__.py            # Pydantic validation models
  │   ├── ml/
  │   │   └── engine.py              # ML models (XGBoost, Isolation Forest)
  │   └── api/
  │       ├── analysis_routes.py     # Credit analysis endpoints
  │       └── simulator_routes.py    # Simulator endpoints
  └── Dockerfile           # Container configuration
```

**Key Features:**
- RESTful API design
- Async request handling
- Pydantic input validation
- SQLAlchemy ORM for type safety
- Comprehensive error handling
- Health check endpoints
- Connection pooling (10 connections)

---

### Database Schema

#### BorrowerProfile Table
```sql
CREATE TABLE borrower_profile (
  id UUID PRIMARY KEY,
  full_name VARCHAR(255) NOT NULL,
  occupation VARCHAR(255),
  employment_type ENUM(salaried, government, business, self_employed, freelancer, unemployed),
  annual_income FLOAT NOT NULL,
  monthly_expenses FLOAT NOT NULL,
  upi_transactions_per_month INT DEFAULT 0,
  payment_history_score FLOAT DEFAULT 0 (0-100),
  savings_behavior_score FLOAT DEFAULT 5 (1-10),
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW(),
  is_active BOOLEAN DEFAULT TRUE
);
-- Indexes: full_name, employment_type, created_at, is_active
```

#### CreditAnalysis Table
```sql
CREATE TABLE credit_analysis (
  id UUID PRIMARY KEY,
  borrower_id UUID FOREIGN KEY,
  credit_score INT (300-900),
  risk_level ENUM(Low, Medium, High),
  default_probability FLOAT (0-1),
  fraud_score FLOAT (0-100),
  is_flagged BOOLEAN,
  loan_approved BOOLEAN,
  recommended_loan_amount FLOAT,
  interest_rate FLOAT,
  interest_band VARCHAR(10),
  loan_category VARCHAR(50),
  shap_values JSONB,
  explanation TEXT,
  improvement_tips JSONB,
  input_data JSONB,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);
-- Indexes on borrower_id, created_at
```

---

## 🤖 ML Pipeline

### 1. Credit Scoring Model
**Type:** XGBoost Regression
**Input Features (6):**
- annual_income
- monthly_expenses
- upi_transactions_per_month
- payment_history_score
- savings_behavior_score
- employment_type (encoded)

**Processing:**
1. Feature engineering
2. StandardScaler normalization
3. XGBoost prediction
4. Clamp output to 300-900 range

**Output:** Credit Score (300-900)

### 2. Fraud Detection Model
**Type:** Isolation Forest (Unsupervised Anomaly Detection)
**Input Features:** Same 6 features as credit scoring

**Processing:**
1. Feature normalization
2. Isolation Forest scoring
3. Anomaly detection
4. Fraud score mapping (0-100)

**Output:** 
- fraud_score (0-100)
- is_flagged (boolean)

### 3. Default Risk Model
**Type:** Random Forest Classification
**Target Classes:** Low, Medium, High Risk

**Processing:**
1. Feature scaling
2. Random Forest prediction
3. Probability extraction

**Output:** Default probability distribution

### 4. SHAP Explainability
**Framework:** SHAP (SHapley Additive exPlanations)
**Method:** Tree Explainer for XGBoost

**Processing:**
1. SHAP value calculation
2. Feature contribution analysis
3. Positive/negative impact determination
4. Score normalization

**Output:**
```json
[
  {
    "feature": "annual_income",
    "contribution": 45.23,
    "direction": "positive",
    "description": "Positive impact on score"
  },
  ...
]
```

---

## 🔄 Request Flow

### Example: Credit Analysis Request

```
┌─────────────────────────────────────────────────────────────┐
│ Client (Frontend)                                           │
│ POST /v1/analyze/instant                                   │
│ {                                                           │
│   "full_name": "John Doe",                                 │
│   "employment_type": "salaried",                           │
│   "annual_income": 1200000,                                │
│   ...                                                       │
│ }                                                           │
└─────────────────┬───────────────────────────────────────────┘
                  │
                  ▼ Validation (Pydantic)
┌─────────────────────────────────────────────────────────────┐
│ FastAPI Route Handler (analysis_routes.py)                 │
└─────────────────┬───────────────────────────────────────────┘
                  │
                  ▼ Feature Engineering
┌─────────────────────────────────────────────────────────────┐
│ ML Engine                                                   │
│ 1. Prepare feature vector                                  │
│ 2. Run Credit Score Model (XGBoost)                        │
│ 3. Run Fraud Detection (Isolation Forest)                  │
│ 4. Determine Risk Level                                    │
│ 5. Calculate Loan Recommendation                           │
│ 6. Generate SHAP Explanations                              │
│ 7. Create Improvement Tips                                 │
└─────────────────┬───────────────────────────────────────────┘
                  │
                  ▼ Database Storage
┌─────────────────────────────────────────────────────────────┐
│ SQLAlchemy ORM                                              │
│ INSERT INTO credit_analysis (...)                          │
│ VALUES (...)                                               │
└─────────────────┬───────────────────────────────────────────┘
                  │
                  ▼ JSON Response
┌─────────────────────────────────────────────────────────────┐
│ Client Response (InstantAnalysisResponse)                  │
│ {                                                           │
│   "credit_score": 745,                                     │
│   "risk_level": "Medium",                                  │
│   "fraud_score": 15.3,                                     │
│   "is_flagged": false,                                     │
│   "loan_approved": true,                                   │
│   "recommended_loan_amount": 600000,                       │
│   "interest_rate": 9.5,                                    │
│   "shap_values": [...],                                    │
│   "explanation": "...",                                    │
│   "improvement_tips": [...]                                │
│ }                                                           │
└─────────────────────────────────────────────────────────────┘
```

---

## 🔐 Security Architecture

### API Security
```
Request → Rate Limiter → CORS Check → Authentication → Validation → Handler
```

### Data Security
- Input validation (Pydantic)
- SQL injection prevention (SQLAlchemy ORM)
- HTTPS in production
- Database encryption at rest

### Authentication (Future)
- JWT tokens
- Role-based access control (RBAC)
- API key management

---

## 📊 Performance Characteristics

### API Response Times (Target)
- Instant Analysis: <500ms
- Database Query: <100ms
- ML Prediction: <200ms
- API Total: <500ms

### Database Performance
- Connection pool size: 10
- Max overflow: 20
- Query timeout: 30s
- Index coverage: All WHERE clauses

### Scalability
- Horizontal scaling ready (stateless API)
- Database replication support
- Caching layer ready (Redis)
- Load balancer compatible

---

## 🚀 Deployment Topology

```
Internet
    │
    ▼
┌───────────────┐
│ Load Balancer │
└───────┬───────┘
        │
    ┌───┴───┬───┬───┐
    │       │   │   │
    ▼       ▼   ▼   ▼
┌─────┐ ┌─────┐ ┌─────┐
│ FE1 │ │ FE2 │ │ BE1 │ (Multiple instances)
└─────┘ └─────┘ └─────┘
                 ┌─────┐
                 │ BE2 │
                 └──┬──┘
                    │
                    ▼
            ┌──────────────┐
            │  PostgreSQL  │
            │  (Primary)   │
            └──────────────┘
                    │
                    ▼
            ┌──────────────┐
            │  PostgreSQL  │
            │  (Replicas)  │
            └──────────────┘
```

---

## 🔧 Technology Stack Summary

| Layer | Technology | Purpose |
|-------|-----------|---------|
| Frontend | Next.js 15, React 18, TypeScript | Web UI |
| API | FastAPI, Uvicorn | REST endpoints |
| Database | PostgreSQL 15, SQLAlchemy | Data persistence |
| ML | XGBoost, Scikit-learn, SHAP | Predictions |
| Container | Docker, Docker Compose | Deployment |
| Styling | TailwindCSS, Framer Motion | UI design |
| i18n | React Context API | Multilingual |

---

## 📈 Roadmap

### Phase 1 (Current - v1.0.0)
- ✅ Core ML models
- ✅ REST API
- ✅ React frontend
- ✅ PostgreSQL database
- ✅ Docker deployment

### Phase 2 (Future - v1.1.0)
- [ ] Redis caching layer
- [ ] JWT authentication
- [ ] Advanced fraud detection
- [ ] Real-time WebSocket updates
- [ ] GraphQL API option

### Phase 3 (Future - v2.0.0)
- [ ] Deep learning models (Neural Networks)
- [ ] Kubernetes orchestration
- [ ] Mobile app
- [ ] Advanced analytics dashboard
- [ ] Multi-tenant support

---

**Last Updated:** 2024
**Version:** 1.0.0
**Status:** Production Ready
