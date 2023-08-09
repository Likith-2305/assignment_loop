from sqlmodel import create_engine, SQLModel, Session
from config import database

#DATABASE_URL = "postgresql://postgres:password@localhost:5432/postgres"
params = database()
DATABASE_URL = f"postgresql://{params['user']}:{params['password']}@{params['host']}:{params['port']}/{params['database']}"
print(DATABASE_URL)

engine = create_engine(DATABASE_URL, echo=True)

def get_session():
    with Session(engine) as session:
        yield session