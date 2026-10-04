import os
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import  declarative_base

db_url= os.getenv("DATABASE_URL","postgresql://postgres:Sarthak2002@localhost:5432/rag_chat")
engine = create_engine(db_url)  
session = sessionmaker(autoflush=False, bind=engine , autocommit = False )
Base = declarative_base()


def getDb():
    db = session()
    try:
        yield db
    finally:
        db.close()