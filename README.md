# FinTrust AI - Complete Project Setup Guide

## 🚀 Quick Start (Recommended - with Docker)

### Prerequisites
- Docker & Docker Compose installed
- Ports 3000, 8000, 5432 available

### Steps

1. **Navigate to project root**
   ```bash
   cd /Users/vishal/fin
   ```

2. **Make setup script executable**
   ```bash
   chmod +x setup.sh
   ```

3. **Run setup script**
   ```bash
   ./setup.sh
   ```

4. **Access the platform**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Docs: http://localhost:8000/api/docs

---

## 📋 Manual Docker Setup

```bash
# Build and start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down

# Stop and remove volumes (WARNING: deletes database)
docker-compose down -v
```

---

## 💻 Local Development (without Docker)

### Backend Setup

```bash
cd /Users/vishal/fin/backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your PostgreSQL details

# Run server
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Setup

```bash
cd /Users/vishal/fin/frontend

# Install dependencies
npm install

# Set environment (optional)
echo "NEXT_PUBLIC_API_URL=http://localhost:8000" > .env.local

# Run development server
npm run dev
```

---

## 📁 Project Structure

```
/Users/vishal/fin/
├── docker-compose.yml          # Main orchestration
├── setup.sh                     # Quick setup script
├── README.md                    # This file
│
├── backend/
│   ├── main.py                 # FastAPI entry point
│   ├── requirements.txt         # Python dependencies
│   ├── Dockerfile              # Backend container config
│   ├── docker-compose.yml      # Backend-specific config
│   │
│   └── app/
│       ├── core/               # Config & database
│       │   ├── config.py
│       │   └── database.py
│       ├── models/             # SQLAlchemy ORM models
│       │   ├── borrower.py
│       │   ├── analysis.py
│       │   ├── transaction.py
│       │   └── payment_history.py
│       ├── schemas/            # Pydantic validation models
│       ├── ml/                 # Machine learning engine
│       │   └── engine.py
│       └── api/                # API routes
│           ├── analysis_routes.py
│           └── simulator_routes.py
│
└── frontend/
    ├── package.json             # Node dependencies
    ├── tsconfig.json            # TypeScript config
    ├── tailwind.config.ts       # TailwindCSS config
    ├── Dockerfile              # Frontend container
    ├── globals.css              # Global styles
    │
    ├── app/                    # Next.js app directory
    │   ├── page.tsx            # Home page
    │   ├── layout.tsx          # Root layout
    │   ├── dashboard/          # Dashboard page
    │   ├── analysis/           # Credit analysis page
    │   └── simulator/          # Simulator page
    │
    └── src/
        ├── contexts/           # React contexts
        ├── services/           # API client
        └── utils/              # Helper functions
```

---

## 🔧 Key Endpoints

### Analysis API
```
POST   /v1/analyze/instant              - Quick analysis
POST   /v1/borrowers                    - Create borrower
GET    /v1/borrowers/{id}               - Get borrower
GET    /v1/borrowers                    - List borrowers
PUT    /v1/borrowers/{id}               - Update borrower
POST   /v1/analyze/{borrower_id}        - Analyze borrower
GET    /v1/analyze/{borrower_id}        - Get analysis
DELETE /v1/borrowers/{id}               - Delete borrower
GET    /v1/portfolio/statistics         - Portfolio stats
```

### Simulator API
```
POST   /v1/simulator/credit-score-simulator       - Credit simulator
POST   /v1/simulator/fraud-detection-simulator    - Fraud detector
POST   /v1/simulator/loan-eligibility-simulator   - Loan check
```

### Health & Info
```
GET    /health                          - Health check
GET    /api/v1/health                   - Detailed health
GET    /api/v1/info                     - API info
```

---

## 🧪 Testing the API

### Create Borrower
```bash
curl -X POST "http://localhost:8000/v1/borrowers" \
  -H "Content-Type: application/json" \
  -d '{
    "full_name": "John Doe",
    "employment_type": "salaried",
    "annual_income": 1200000,
    "monthly_expenses": 50000,
    "payment_history_score": 85,
    "savings_behavior_score": 8
  }'
```

### Quick Analysis
```bash
curl -X POST "http://localhost:8000/v1/analyze/instant" \
  -H "Content-Type: application/json" \
  -d '{
    "full_name": "Jane Smith",
    "employment_type": "self_employed",
    "annual_income": 1800000,
    "monthly_expenses": 75000,
    "payment_history_score": 90,
    "savings_behavior_score": 9
  }'
```

### Credit Simulator
```bash
curl -X POST "http://localhost:8000/v1/simulator/credit-score-simulator" \
  -H "Content-Type: application/json" \
  -d '{
    "full_name": "Test User",
    "employment_type": "salaried",
    "annual_income": 1000000,
    "monthly_expenses": 40000
  }'
```

---

## 📊 Features Implemented

### Backend Features
✅ XGBoost Credit Score Model (300-900)
✅ Fraud Detection (Isolation Forest)
✅ Default Risk Prediction (Random Forest)
✅ SHAP Explainability
✅ Loan Approval Engine
✅ Interest Rate Recommendations
✅ What-if Scenarios
✅ Portfolio Analytics
✅ Borrower Profile Management
✅ RESTful API with FastAPI
✅ PostgreSQL Database
✅ ORM with SQLAlchemy

### Frontend Features
✅ Dashboard with Portfolio Analytics
✅ Credit Analysis Interface
✅ What-if Simulator
✅ Fraud Detection Display
✅ Real-time Updates
✅ Multilingual Support (EN/HI)
✅ Responsive Design
✅ SHAP Explainability Visualization
✅ Improvement Recommendations
✅ Risk Indicators

---

## 🗄️ Database Schema

### BorrowerProfile
- id, full_name, occupation, employment_type
- annual_income, monthly_expenses
- upi_transactions_per_month, payment_history_score
- savings_behavior_score, created_at, updated_at, is_active

### CreditAnalysis
- id, borrower_id, credit_score, risk_level
- default_probability, fraud_score, is_flagged
- loan_approved, recommended_loan_amount, interest_rate
- shap_values, explanation, improvement_tips
- created_at, updated_at

### Transaction
- id, borrower_id, transaction_type, amount
- description, transaction_date, created_at

### PaymentHistory
- id, borrower_id, bill_type, due_date
- payment_date, amount, is_paid, days_late

---

## 🔒 Production Deployment

### Environment Setup
```bash
# Copy .env.example to .env
cp backend/.env.example backend/.env

# Update with production values:
DEBUG=False
CORS_ORIGINS=["https://yourdomain.com"]
DATABASE_URL=postgresql://user:pass@prod-db:5432/db
SECRET_KEY=<generate-random-secret>
```

### Using Gunicorn (Backend)
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 main:app
```

### Using PM2 / Docker for Production
```bash
docker build -t fintrust-backend backend/
docker run -d -p 8000:8000 --env-file backend/.env fintrust-backend
```

---

## 📈 ML Models

### Credit Score Model (XGBoost)
- Input: Annual income, expenses, transactions, payment history, savings behavior, employment type
- Output: Credit Score (300-900)
- Features: 6 numerical/categorical inputs
- Training data: 100 synthetic samples

### Fraud Detection (Isolation Forest)
- Input: Financial transaction patterns
- Output: Fraud score (0-100), is_anomaly (boolean)
- Contamination rate: 10%
- Features: Detection of transaction anomalies

### Default Risk (Random Forest)
- Input: Borrower financial metrics
- Output: Default probability (0-1)
- Classes: Low, Medium, High risk
- Training samples: Balanced classes

### SHAP Explainability
- Explains contribution of each feature to credit score
- Shows positive/negative impact
- Provides actionable improvement tips

---

## 🐛 Troubleshooting

### Port Already in Use
```bash
# Change port in docker-compose.yml or:
lsof -i :3000          # Find process using port 3000
kill -9 <PID>          # Kill process
```

### Database Connection Error
- Verify PostgreSQL is running
- Check DATABASE_URL in .env
- Ensure credentials are correct
- Check network connectivity

### API Not Responding
```bash
# Check backend logs
docker-compose logs backend

# Check if backend container is running
docker ps

# Verify API is accessible
curl http://localhost:8000/health
```

### Frontend Not Loading
```bash
# Check frontend logs
docker-compose logs frontend

# Verify NEXT_PUBLIC_API_URL is correct
# Rebuild frontend
docker-compose build frontend
```

### Build Errors
```bash
# Clean and rebuild
docker-compose down -v
docker system prune -a
docker-compose up -d --build
```

---

## 📚 Additional Resources

- **API Documentation**: http://localhost:8000/api/docs
- **ReDoc**: http://localhost:8000/api/redoc
- **OpenAPI Spec**: http://localhost:8000/api/openapi.json
- **Backend Repo**: ./backend/README.md
- **Frontend Repo**: ./frontend/README.md

---

## 🤝 Support

For issues or questions:
1. Check logs: `docker-compose logs -f`
2. Verify environment variables
3. Ensure all services are running: `docker-compose ps`
4. Check database connectivity

---

## 📝 License

FinTrust AI - Intelligent Fintech Platform
Version 1.0.0

All rights reserved. © 2024 FinTrust AI Team
# fintrust
