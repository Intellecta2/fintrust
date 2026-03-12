# FinTrust AI Backend - Setup Instructions

## Quick Start (Docker)

### Prerequisites
- Docker and Docker Compose installed
- Git

### Setup Steps

1. **Clone or create the project**
   ```bash
   cd /Users/vishal/fin/backend
   ```

2. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration if needed
   ```

3. **Start services with Docker Compose**
   ```bash
   docker-compose up -d
   ```

4. **Access the API**
   - API: http://localhost:8000
   - API Docs: http://localhost:8000/api/docs
   - ReDoc: http://localhost:8000/api/redoc

### Verify Setup
```bash
curl http://localhost:8000/health
```

---

## Local Development (without Docker)

### Prerequisites
- Python 3.11+
- PostgreSQL 15+

### Setup Steps

1. **Create virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure database**
   - Install PostgreSQL locally
   - Create database: `createdb fintrust_db`
   - Update DATABASE_URL in .env

4. **Run migrations (if using Alembic)**
   ```bash
   alembic upgrade head
   ```

5. **Start the application**
   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

6. **Access the API**
   - API: http://localhost:8000
   - API Docs: http://localhost:8000/api/docs

---

## API Endpoints

### Analysis Endpoints
- `POST /v1/analyze/instant` - Quick credit analysis without saving profile
- `POST /v1/borrowers` - Create borrower profile
- `GET /v1/borrowers/{borrower_id}` - Get borrower profile
- `GET /v1/borrowers` - List all borrowers
- `PUT /v1/borrowers/{borrower_id}` - Update borrower profile
- `POST /v1/analyze/{borrower_id}` - Perform credit analysis
- `GET /v1/analyze/{borrower_id}` - Get latest analysis
- `DELETE /v1/borrowers/{borrower_id}` - Soft delete borrower
- `GET /v1/portfolio/statistics` - Portfolio analytics

### Simulator Endpoints
- `POST /v1/simulator/credit-score-simulator` - What-if credit score simulator
- `POST /v1/simulator/fraud-detection-simulator` - Fraud detection simulator
- `POST /v1/simulator/loan-eligibility-simulator` - Loan eligibility checker

### Health & Info
- `GET /health` - Basic health check
- `GET /api/v1/health` - Detailed health check with DB status
- `GET /api/v1/info` - API information and endpoints

---

## Testing the API

### Create Borrower Profile
```bash
curl -X POST "http://localhost:8000/v1/borrowers" \
  -H "Content-Type: application/json" \
  -d '{
    "full_name": "John Doe",
    "occupation": "Software Engineer",
    "employment_type": "salaried",
    "annual_income": 1200000,
    "monthly_expenses": 50000,
    "upi_transactions_per_month": 45,
    "payment_history_score": 85,
    "savings_behavior_score": 8
  }'
```

### Instant Analysis (No Profile Needed)
```bash
curl -X POST "http://localhost:8000/v1/analyze/instant" \
  -H "Content-Type: application/json" \
  -d '{
    "full_name": "Jane Smith",
    "occupation": "Doctor",
    "employment_type": "self_employed",
    "annual_income": 1800000,
    "monthly_expenses": 75000,
    "upi_transactions_per_month": 60,
    "payment_history_score": 90,
    "savings_behavior_score": 9
  }'
```

### Credit Score Simulator
```bash
curl -X POST "http://localhost:8000/v1/simulator/credit-score-simulator" \
  -H "Content-Type: application/json" \
  -d '{
    "full_name": "Test User",
    "employment_type": "salaried",
    "annual_income": 1000000,
    "monthly_expenses": 40000,
    "upi_transactions_per_month": 30,
    "payment_history_score": 75,
    "savings_behavior_score": 6
  }'
```

---

## Features Implemented

✅ XGBoost Credit Score Model (300-900)
✅ Fraud Detection with Isolation Forest
✅ Default Risk Prediction
✅ SHAP Explainability
✅ Loan Approval Decision Engine
✅ Interest Rate Recommendation
✅ Portfolio Analytics
✅ What-if Simulator
✅ RESTful API with FastAPI
✅ PostgreSQL Database with ORM
✅ Docker & Docker Compose Setup

---

## Production Deployment

### Environment Variables to Update
```
DEBUG=False
DATABASE_URL=postgresql://user:password@prod-db:5432/fintrust_db
CORS_ORIGINS=["https://yourdomain.com"]
SECRET_KEY=<generate-secure-random-key>
ENCRYPTION_KEY=<generate-secure-random-key>
```

### Run with Gunicorn
```bash
gunicorn -w 4 -b 0.0.0.0:8000 main:app
```

---

## Troubleshooting

**Port already in use:**
```bash
# Change port in .env or use:
docker-compose -f docker-compose.yml down
```

**Database connection error:**
- Verify PostgreSQL is running
- Check DATABASE_URL in .env
- Verify credentials

**ML Models not found:**
- Models are generated on first run
- Check /models directory for pickle files

---

## Support & Documentation

- API Documentation: http://localhost:8000/api/docs
- OpenAPI Spec: http://localhost:8000/api/openapi.json
- ReDoc: http://localhost:8000/api/redoc

---

## License & Authors

FinTrust AI - Intelligent Fintech Platform
Version 1.0.0
