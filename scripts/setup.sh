#!/bin/bash
set -e

echo "=== Operations Command Center Setup ==="

# Backend
echo "[1/3] Setting up backend..."
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cd ..

# Frontend
echo "[2/3] Setting up frontend..."
cd frontend
npm install
cd ..

echo "[3/3] Setup complete!"
echo ""
echo "To run with Docker:  docker compose up"
echo "To run manually:"
echo "  Backend:  cd backend && source venv/bin/activate && uvicorn app.main:app --reload"
echo "  Frontend: cd frontend && npm run dev"
echo ""
echo "Make sure PostgreSQL is running with database 'opscenter'"
echo "Seed data: psql -U postgres -d opscenter -f data/seed_data.sql"
