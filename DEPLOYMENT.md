# FinTrust AI - Deployment Guide

## 📦 Pre-Deployment Checklist

- [ ] Docker & Docker Compose installed
- [ ] Sufficient disk space (5GB+)
- [ ] Ports 3000, 8000, 5432 available
- [ ] Environment variables configured
- [ ] Database credentials set

---

## 🚀 Deployment Methods

### Method 1: Automated Setup (Recommended)

```bash
cd /Users/vishal/fin
chmod +x setup.sh
./setup.sh
```

**Time**: ~1-2 minutes
**Effort**: Minimal

### Method 2: Docker Compose Manual

```bash
cd /Users/vishal/fin
docker-compose up -d
```

**Time**: ~1-2 minutes
**Effort**: Minimal

### Method 3: Local Development

**Backend:**
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn main:app --reload
# Access: http://localhost:8000
```

**Frontend:**
```bash
cd frontend
npm install
npm run dev
# Access: http://localhost:3000
```

---

## 🔧 Production Deployment

### Environment Setup

Create `backend/.env` with production values:

```env
DEBUG=False
API_HOST=0.0.0.0
API_PORT=8000

# Database (use production PostgreSQL)
DATABASE_URL=postgresql://prod_user:strong_password@prod-db.example.com:5432/fintrust_db

# CORS
CORS_ORIGINS=["https://yourdomain.com"]

# Security
SECRET_KEY=your-long-random-secret-key-here
ENCRYPTION_KEY=your-encryption-key-here
```

### Using Docker (Production)

```bash
# Build images with production Dockerfile
docker build -t fintrust-backend:latest backend/
docker build -t fintrust-frontend:latest frontend/

# Run with docker-compose
docker-compose -f docker-compose.yml up -d
```

### Using Kubernetes

```bash
# Create namespace
kubectl create namespace fintrust

# Apply manifests (create k8s/ directory with manifests)
kubectl apply -f k8s/ -n fintrust

# View status
kubectl get pods -n fintrust
```

### Using AWS/Cloud Platform

**AWS ECS:**
```bash
# Push to ECR
aws ecr get-login-password | docker login --username AWS --password-stdin $AWS_ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com

docker tag fintrust-backend:latest $AWS_ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com/fintrust-backend:latest
docker push $AWS_ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com/fintrust-backend:latest

# Create ECS task definitions and services
```

---

## 🔒 Security Considerations

### API Security
- Enable HTTPS/SSL in production
- Implement API rate limiting
- Use API keys/JWT authentication
- Enable CORS only for trusted domains
- Add WAF (Web Application Firewall)

### Database Security
- Use strong passwords (minimum 32 characters)
- Enable SSL connections to database
- Regular backups (daily minimum)
- Restrict database access to application servers only
- Enable database audit logging

### Frontend Security
- Use Content Security Policy (CSP) headers
- Enable Secure cookies (HttpOnly, Secure flags)
- Implement environment variable validation
- Never expose secrets in frontend code

### Application Security
- Regular dependency updates
- Security scanning (OWASP, Snyk)
- Input validation on all endpoints
- SQL injection prevention (using ORM)
- CSRF protection

---

## 📊 Monitoring & Logging

### Logs Collection

```bash
# View backend logs
docker-compose logs backend

# View frontend logs
docker-compose logs frontend

# View database logs
docker-compose logs postgres

# Follow real-time logs
docker-compose logs -f
```

### Health Checks

```bash
# Backend health
curl http://localhost:8000/health

# API health with DB status
curl http://localhost:8000/api/v1/health

# Frontend health
curl http://localhost:3000
```

### Metrics to Monitor

- API response time (target: <200ms)
- Database query performance (target: <100ms)
- Memory usage (target: <500MB per service)
- CPU usage (target: <50%)
- Request success rate (target: >99.9%)

---

## 🔄 Backup & Recovery

### Database Backup

```bash
# Backup PostgreSQL
docker exec fintrust_postgres pg_dump -U fintrust fintrust_db > backup.sql

# Restore from backup
docker exec -i fintrust_postgres psql -U fintrust fintrust_db < backup.sql

# Automated daily backup script
0 2 * * * docker exec fintrust_postgres pg_dump -U fintrust fintrust_db > /backups/fintrust_$(date +\%Y\%m\%d).sql
```

### Model Backups

```bash
# Backup ML models
tar -czf models_backup_$(date +%Y%m%d).tar.gz backend/models/

# Store in S3 or cloud storage for safety
aws s3 cp models_backup_*.tar.gz s3://your-bucket/backups/
```

---

## 📈 Scaling

### Horizontal Scaling

```yaml
# Update docker-compose.yml for multiple instances
services:
  backend:
    deploy:
      replicas: 3
  frontend:
    deploy:
      replicas: 2
```

### Load Balancing

```bash
# Using Nginx as reverse proxy
upstream backend {
  server backend:8000;
  server backend-2:8000;
  server backend-3:8000;
}

server {
  listen 80;
  location /api {
    proxy_pass http://backend;
  }
}
```

---

## 🆘 Troubleshooting

### Service Won't Start

```bash
# Check logs
docker-compose logs --tail=100

# Rebuild
docker-compose down -v
docker-compose up -d --build

# Check resource usage
docker stats
```

### Database Connection Issues

```bash
# Test connection
docker exec -it fintrust_postgres psql -U fintrust -d fintrust_db -c "SELECT 1"

# Check connection pool
netstat -an | grep 5432
```

### API Timeouts

```bash
# Increase timeout in nginx/proxy
proxy_read_timeout 30s;
proxy_connect_timeout 10s;

# Check database queries
docker exec -it fintrust_postgres psql -U fintrust -d fintrust_db -c "SELECT * FROM pg_stat_statements"
```

---

## 📋 Post-Deployment Checklist

- [ ] Services running (`docker-compose ps`)
- [ ] Database connectivity verified
- [ ] API responding (`curl http://localhost:8000/health`)
- [ ] Frontend accessible (`curl http://localhost:3000`)
- [ ] Logs monitored for errors
- [ ] Backups configured
- [ ] Security settings verified
- [ ] Monitoring alerts set up
- [ ] Documentation updated
- [ ] Team trained on operations

---

## 🆔 Useful Commands

```bash
# System info
docker-compose ps
docker system df
docker stats

# Database
docker exec -it fintrust_postgres psql -U fintrust -d fintrust_db
SELECT version();  -- Check PostgreSQL version

# Logs
docker-compose logs -f --tail=50

# Restart services
docker-compose restart

# Clean up
docker-compose down -v
docker system prune -a

# Update images
docker-compose pull
docker-compose up -d
```

---

## 📞 Support

For deployment issues:
1. Check logs: `docker-compose logs -f`
2. Verify environment variables
3. Test connectivity to all services
4. Review security settings
5. Check disk space and resources

---

## 📝 Version History

- **v1.0.0** - Initial production release
  - Full ML model implementation
  - Complete REST API
  - React frontend
  - Docker deployment
  - PostgreSQL database

---

**Last Updated: 2024**
**For questions contact: FinTrust AI Team**
