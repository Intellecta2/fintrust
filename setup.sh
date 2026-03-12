#!/bin/bash

# FinTrust AI - Complete Setup Script
# This script sets up and runs the entire FinTrust AI platform

set -e

echo "================================================"
echo "  FinTrust AI - Intelligent Fintech Platform"
echo "  Setup & Deployment Script"
echo "================================================"
echo ""

# Check Docker
if ! command -v docker &> /dev/null; then
    echo "Error: Docker is not installed. Please install Docker first."
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "Error: Docker Compose is not installed"
    exit 1
fi

echo "✓ Docker and Docker Compose found"
echo ""

# Create directories if they don't exist
echo "Setting up project structure..."
mkdir -p backend frontend
echo "✓ Project directories ready"
echo ""

# Check if backend and frontend exist
if [ ! -f "backend/main.py" ]; then
    echo "Warning: Backend files not found. Please ensure backend code is in ./backend"
fi

if [ ! -f "frontend/package.json" ]; then
    echo "Warning: Frontend files not found. Please ensure frontend code is in ./frontend"
fi

echo ""
echo "================================================"
echo "  Starting FinTrust AI Services"
echo "================================================"
echo ""

# Start services
echo "Building and starting Docker containers..."
docker-compose up -d

echo ""
echo "✓ Services started successfully!"
echo ""
echo "================================================"
echo "  FinTrust AI is Running!"
echo "================================================"
echo ""
echo "📍 Frontend:   http://localhost:3000"
echo "📍 Backend:    http://localhost:8000"
echo "📍 API Docs:   http://localhost:8000/api/docs"
echo "📍 PgAdmin:    http://localhost:5050 (optional - use 'docker-compose --profile debug up')"
echo ""
echo "🔑 Database Credentials:"
echo "   User: fintrust"
echo "   Password: fintrust_secure_password"
echo "   Database: fintrust_db"
echo ""
echo "📊 Access the application at http://localhost:3000"
echo ""
echo "To view logs: docker-compose logs -f"
echo "To stop services: docker-compose down"
echo ""
