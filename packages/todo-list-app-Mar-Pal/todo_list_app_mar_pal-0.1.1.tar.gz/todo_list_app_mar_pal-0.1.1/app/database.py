from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import Base  
from app.config import settings

DATABASE_URL = settings.DATABASE_URL

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine) 