from sqlalchemy import create_engine

DATABASE_URL = "sqlite:///intelligence.db"

engine = create_engine(
    DATABASE_URL,
    echo=False
)
