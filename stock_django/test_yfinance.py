import yfinance as yf
import json

def test_yfinance():
    # Test with Technology Sector ETF (XLK)
    ticker_symbol = "XLK" 
    ticker = yf.Ticker(ticker_symbol)
    
    print(f"--- Testing {ticker_symbol} ---")
    
    # 1. Price History (for charts)
    hist = ticker.history(period="5d")
    print(f"\n[Price History (Last 5 days)]")
    if not hist.empty:
        print(hist[['Close']].tail())
    else:
        print("No history found.")

    # 2. News
    print(f"\n[News]")
    news = ticker.news
    if news:
        for item in news[:2]:
            print(f"- {item.get('title')} ({item.get('publisher')})")
    else:
        print("No news found.")

    # 3. Current Info (for % change)
    # info = ticker.info # info can be slow/unreliable sometimes, let's check basic fields
    # print(f"\n[Info]")
    # print(f"Previous Close: {info.get('previousClose')}")

if __name__ == "__main__":
    test_yfinance()
