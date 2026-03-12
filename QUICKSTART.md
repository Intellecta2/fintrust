# FinTrust AI - Quick Start Guide

## 🎯 5-Minute Setup

### Prerequisites
- Docker & Docker Compose installed
- Ports 3000, 8000, 5432 available

### Quick Start

```bash
# 1. Navigate to project
cd /Users/vishal/fin

# 2. Make setup script executable
chmod +x setup.sh

# 3. Run setup (builds and starts all services)
./setup.sh

# 4. Wait for services to start (1-2 minutes)

# 5. Open browser
open http://localhost:3000
```

**That's it! 🎉**

---

## 📍 Access Points

| Service | URL | Purpose |
|---------|-----|---------|
| Frontend | http://localhost:3000 | Main application |
| Backend | http://localhost:8000 | API server |
| API Docs | http://localhost:8000/api/docs | Swagger UI |
| ReDoc | http://localhost:8000/api/redoc | ReDoc docs |
| PgAdmin | http://localhost:5050 | Database UI (optional) |

---

## 🧪 Try It Out

### 1. Analyze a Borrower (Instant)
Visit: http://localhost:3000/analysis
- Fill in the borrower information
- Click "Analyze Credit"
- See credit score, fraud detection, and loan recommendations

### 2. Run What-if Simulator
Visit: http://localhost:3000/simulator
- Adjust income, expenses, payment history
- Run different scenarios
- See impact on credit score

### 3. View Portfolio Analytics
Visit: http://localhost:3000/dashboard
- See aggregate statistics
- View risk distribution
- Monitor fraud alerts

---

## 🛠️ Common Commands

```bash
# View live logs
docker-compose logs -f

# View specific service logs
docker-compose logs -f backend
docker-compose logs -f frontend

# Stop all services
docker-compose down

# Stop and remove volumes (CAREFUL - deletes database)
docker-compose down -v

# Restart services
docker-compose restart

# See running containers
docker-compose ps
```

---

## 📚 Example API Calls

### Test with curl

```bash
# Health check
curl http://localhost:8000/health

# Create borrower profile
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

# Quick analysis (no profile needed)
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

---

## 🔑 Database Credentials

When needed for debugging:
```
Host: localhost
Port: 5432
User: fintrust
Password: fintrust_secure_password
Database: fintrust_db
```

---

## ❌ Troubleshooting

**Services won't start?**
```bash
# Rebuild everything
docker-compose down -v
docker-compose up -d --build
```

**Port already in use?**
```bash
# Kill process using port
lsof -i :3000          # Find process
kill -9 <PID>          # Kill it
```

**Check if services are healthy**
```bash
docker-compose ps    # See all containers
curl http://localhost:8000/health  # Check backend
```

---

## 📖 Documentation

- Full setup guide: [README.md](./README.md)
- Backend docs: [backend/README.md](./backend/README.md)
- Frontend docs: [frontend/README.md](./frontend/README.md)
- API docs: http://localhost:8000/api/docs (when running)

---

## 🎓 Features to Explore

1. **Credit Scoring** - See how various financial metrics impact credit score
2. **Fraud Detection** - SHAP values explain why a credit might be flagged
3. **What-if Analysis** - Test different financial scenarios instantly
4. **Portfolio Analytics** - Aggregate view of all borrowers and risk
5. **Multilingual Support** - Toggle between English and Hindi
6. **Recommendation Engine** - Get specific tips to improve credit score

---

## 📊 Next Steps

1. Explore the UI at http://localhost:3000
2. Try different scenarios in the simulator
3. Check API docs at http://localhost:8000/api/docs
4. Review backend code in `./backend/app/`
5. Customize ML models for your use case

---

**Happy exploring! 🚀**

For detailed documentation, see [README.md](./README.md)
