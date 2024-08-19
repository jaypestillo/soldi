import pandas as pd
from sqlalchemy import create_engine, Column, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from alpha_vantage.timeseries import TimeSeries
from datetime import time
import os

# Define the SQLite database
DATABASE_URL = "sqlite:///stock_data.db"
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

# Define the base for SQLAlchemy models
Base = declarative_base()

# Define the StockData model
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

# Create the table
Base.metadata.create_all(engine)

# Initialize the Alpha Vantage API
API_KEY = 'your_alpha_vantage_api_key'
ts = TimeSeries(key=API_KEY, output_format='pandas')

def fetch_and_store_stock_data(symbol):
    # Fetch data from Alpha Vantage
    data, _ = ts.get_intraday(symbol=symbol, interval='1min', outputsize='full')

    # Convert index to a column and rename columns
    data.reset_index(inplace=True)
    data.columns = ['date', 'open', 'high', 'low', 'close', 'volume']

    # Filter out non-trading hours (9:30 AM to 4:00 PM)
    data['date'] = pd.to_datetime(data['date'])
    data = data[
        (data['date'].dt.time >= time(9, 30)) &
        (data['date'].dt.time <= time(16, 0)) &
        (data['date'].dt.weekday < 5)  # Exclude weekends
    ]

    # Store the filtered data in the SQLite database
    for index, row in data.iterrows():
        stock_data = StockData(
            id=f"{symbol}_{row['date']}",
            symbol=symbol,
            date=row['date'],
            open=row['open'],
            high=row['high'],
            low=row['low'],
            close=row['close'],
            volume=row['volume']
        )
        session.merge(stock_data)  # Use merge to avoid duplications
    session.commit()

def load_and_filter_stock_data(symbol):
    # Query the database for the stock data
    data = pd.read_sql_query(
        f"SELECT * FROM stock_data WHERE symbol='{symbol}' ORDER BY date", 
        engine
    )

    # Ensure date is a datetime object
    data['date'] = pd.to_datetime(data['date'])

    return data

def fetch_all_tickers():
    # Read tickers from the configuration file
    if not os.path.exists("tickers.txt"):
        print("Tickers configuration file not found.")
        return

    with open("tickers.txt", "r") as file:
        tickers = [line.strip() for line in file if line.strip()]

    for ticker in tickers:
        try:
            print(f"Fetching data for {ticker}...")
            fetch_and_store_stock_data(ticker)
            print(f"Data for {ticker} stored successfully.")
        except Exception as e:
            print(f"Failed to fetch data for {ticker}: {e}")

