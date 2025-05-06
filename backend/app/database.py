import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool

# SQLite URL
SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///./content.db"

# Create async engine
engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False},
    poolclass=NullPool,
)

# Create sessionmaker
async_session = sessionmaker(
    engine, 
    class_=AsyncSession, 
    expire_on_commit=False
)

# Dependency to get DB session
async def get_db():
    async with async_session() as session:
        try:
            yield session
        finally:
            await session.close() 