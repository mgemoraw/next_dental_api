from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker


engine = create_engine("sqlite:///data.db", echo=True)

Session = sessionmaker(bind=engine)
# Base = declarative_base()
