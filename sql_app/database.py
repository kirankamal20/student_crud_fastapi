from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "postgresql+psycopg2://kirankamal45:2ZezcxM9jTJn@ep-lingering-mouse-96266058.ap-southeast-1.aws.neon.tech/kirandatabase"

engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_size=10,
                                      max_overflow=2,
                                      pool_recycle=300,
                                      pool_pre_ping=True,
                                      pool_use_lifo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

 




 
