import feedparser
import json

def test_rss_news():
    # Test with Technology Sector ETF (XLK)
    ticker = "XLK"
    rss_url = f"https://finance.yahoo.com/rss/headline?s={ticker}"
    
    print(f"--- Testing RSS for {ticker} ---")
    feed = feedparser.parse(rss_url)
    
    if feed.entries:
        print(f"Found {len(feed.entries)} entries.")
        for entry in feed.entries[:5]:
            print(f"- Title: {entry.title}")
            print(f"  Link: {entry.link}")
            print(f"  Published: {entry.published}")
            print("-" * 20)
    else:
        print("No entries found in RSS feed.")
        # Print debug info
        if hasattr(feed, 'bozo_exception'):
             print(f"Error: {feed.bozo_exception}")

if __name__ == "__main__":
    test_rss_news()
