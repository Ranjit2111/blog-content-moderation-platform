@echo off
echo Setting up backend...
python -m venv env
call env\Scripts\activate
echo Activated Virtual Environment 
echo Installing backend dependencies...
IF EXIST requirements.txt (
    pip install -r requirements.txt
) ELSE (
    echo Warning: requirements.txt not found, installing essential packages...
    pip install fastapi uvicorn sqlalchemy aiosqlite pydantic alembic google-generativeai python-dotenv
    pip freeze > backend\requirements.txt
    echo Created requirements.txt file in the backend directory
)

echo Setting up database...
cd backend
IF NOT EXIST "content.db" (
    echo Creating database tables...
    python -c "from app.models import Base; from app.database import engine; import asyncio; asyncio.run(async def _(): async with engine.begin() as conn: await conn.run_sync(Base.metadata.create_all)())()"
)
cd ..

echo Setting up frontend...
cd frontend
echo Installing frontend dependencies...
IF EXIST package.json (
    npm install
) ELSE (
    npm init -y
    npm install react react-dom react-router-dom axios
    npm install --save-dev vite @vitejs/plugin-react
)
cd ..

echo Setup complete!
echo To start the application, run runapplication.bat