from collections.abc import Generator
from sqlmodel import Session 
from sqlmodel import create_engine, SQLModel, Session

DATABASE_URL = "sqlite:///./database.db"
engine = create_engine(DATABASE_URL, echo=True)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_db() -> Generator[Session, None, None]:
    with Session(engine) as session:
        try:
            yield session
        finally:
            session.close