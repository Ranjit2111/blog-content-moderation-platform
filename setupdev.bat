@echo off
echo Setting up backend...
python -m venv env
call env\Scripts\activate
pip install fastapi uvicorn sqlalchemy aiosqlite pydantic alembic
cd backend
alembic init migrations
cd ..

echo Setting up frontend...
cd frontend
npm init -y
npm install react react-dom react-router-dom axios vite @vitejs/plugin-react
cd ..

echo Setup complete! 