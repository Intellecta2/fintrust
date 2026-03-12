# FinTrust AI - Intelligent Fintech Platform

This is the main __init__ file for the FinTrust AI application package.

FinTrust AI is a complete, production-grade fintech platform with advanced AI capabilities:

- **XGBoost Credit Scoring** (300-900 scale)
- **Fraud Detection** with Isolation Forest and SHAP explainability
- **Default Risk Prediction** using Random Forest
- **What-if Scenarios** for loan simulation
- **Portfolio Analytics** for aggregate insights
- **REST API** built with FastAPI
- **PostgreSQL Database** with SQLAlchemy ORM
- **Modern Frontend** with Next.js and React

## Project Structure

```
/Users/vishal/fin/
├── backend/              # FastAPI backend with ML models
├── frontend/             # Next.js React frontend
├── docker-compose.yml    # Full stack orchestration
├── setup.sh              # Quick setup script
└── README.md             # Comprehensive guide
```

## Quick Start

```bash
# Run complete setup
chmod +x setup.sh
./setup.sh

# Access at http://localhost:3000
```

## Architecture

### Backend (FastAPI + Python ML)
- Credit score prediction with XGBoost
- Fraud detection with Isolation Forest
- SHAP-based explainability
- RESTful API endpoints
- PostgreSQL database

### Frontend (Next.js + React)
- Dashboard with portfolio analytics
- Credit analysis interface
- What-if simulator
- Real-time updates
- Responsive design

## Documentation

- [Complete README](./README.md)
- [Quick Start](./QUICKSTART.md)
- [Backend Setup](./backend/README.md)
- [Frontend Setup](./frontend/README.md)

## Version

**FinTrust AI v1.0.0**
- Production-grade implementation
- Full ML model integration
- Complete API and UI
- Docker containerization

## License

All rights reserved. © 2024 FinTrust AI Team
