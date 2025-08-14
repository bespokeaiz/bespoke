from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from .config import settings

# По умолчанию (если переменная не задана) используем SQLite в памяти,
# чтобы CI и импорт работали без внешней БД.
DEFAULT_SQLITE = "sqlite+pysqlite:///:memory:"

DATABASE_URL = settings.DATABASE_URL or DEFAULT_SQLITE

engine = create_engine(
    DATABASE_URL,
    echo=False,
    future=True
)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)

class Base(DeclarativeBase):
    pass

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
