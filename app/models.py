from sqlalchemy import create_engine, Column, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class StockData(Base):
    __tablename__ = 'stock_data'
    id = Column(String, primary_key=True)
    symbol = Column(String)
    date = Column(DateTime)
    open = Column(Float)
    high = Column(Float)
    low = Column(Float)
    close = Column(Float)
    volume = Column(Float)

# Set up the database engine with a timeout
engine = create_engine('sqlite:///stocks.db', connect_args={'timeout': 30})
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
