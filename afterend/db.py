from sqlalchemy import create_engine

from sqlalchemy.orm import sessionmaker

# engine = create_engine("sqlite:///database.db", connect_args={"check_same_thread": False})

SQLALCHEMY_DATABASE_URL: str = 'mysql+pymysql://root:12345678@localhost:3306/test-manage?charset=utf8'
engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_pre_ping=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

session = SessionLocal()
