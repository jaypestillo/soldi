from app import app, server
from app.data_fetcher import fetch_all_tickers

if __name__ == "__main__":
    # Fetch data for all tickers on startup
    fetch_all_tickers()

    # Run the Flask server
    server.run(debug=True, port=8050)
