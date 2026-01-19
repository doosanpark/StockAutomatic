from django.shortcuts import render
from django.http import JsonResponse
import yfinance as yf
import feedparser
import pandas as pd
from datetime import datetime

# GICS Sector to ETF Mapping
SECTOR_MAP = {
    '에너지': 'XLE',
    '소재': 'XLB',
    '산업재': 'XLI',
    '임의소비재': 'XLY',
    '필수소비재': 'XLP',
    '헬스케어': 'XLV',
    '금융': 'XLF',
    'IT': 'XLK',
    '통신서비스': 'XLC',
    '유틸리티': 'XLU',
    '부동산': 'XLRE',
}

def get_sector_performance():
    tickers = list(SECTOR_MAP.values())
    # Download 5 days of data to ensure we have previous close even over weekends/holidays
    data = yf.download(tickers, period="5d", progress=False)['Close']
    
    performance = []
    
    # Get the last two valid trading days
    if len(data) >= 2:
        last_price = data.iloc[-1]
        prev_price = data.iloc[-2]
        
        for sector_name, ticker in SECTOR_MAP.items():
            try:
                current = last_price[ticker]
                prev = prev_price[ticker]
                change_pct = ((current - prev) / prev) * 100
                
                performance.append({
                    'name': sector_name,
                    'ticker': ticker,
                    'value': round(change_pct, 2)
                })
            except Exception as e:
                print(f"Error processing {ticker}: {e}")
                
    return performance

def index(request):
    try:
        sector_data = get_sector_performance()
    except Exception as e:
        print(f"Error fetching initial data: {e}")
        sector_data = [] # Fallback or Mock could be used here if needed

    context = {
        'sector_data': sector_data,
    }
    return render(request, 'dashboard/index.html', context)

from deep_translator import GoogleTranslator

# ... (Previous imports) ...

def sector_detail(request, ticker):
    """API endpoint for fetching history and news for a specific sector"""
    try:
        stock = yf.Ticker(ticker)
        
        # 1. Get History (1 Month)
        hist = stock.history(period="1mo")
        dates = hist.index.strftime('%Y-%m-%d').tolist()
        prices = hist['Close'].tolist()
        
        # 2. Get News using RSS (More reliable than yfinance.news)
        rss_url = f"https://finance.yahoo.com/rss/headline?s={ticker}"
        feed = feedparser.parse(rss_url)
        
        # Initialize Translator
        translator = GoogleTranslator(source='auto', target='ko')
        
        news_list = []
        for entry in feed.entries[:10]:
            # Parse date if possible, otherwise keep original string
            try:
                published_time = datetime.strptime(entry.published, "%a, %d %b %Y %H:%M:%S %z")
                date_str = published_time.strftime('%Y-%m-%d')
            except:
                date_str = entry.published[:16] # Fallback
            
            # Translate Title
            try:
                translated_title = translator.translate(entry.title)
            except:
                translated_title = entry.title # Fallback to original if translation fails
            
            news_list.append({
                'title': translated_title,
                'publisher': 'Yahoo Finance', # RSS doesn't always provide publisher name cleanly
                'link': entry.link,
                'thumbnail': '', 
                'date': date_str
            })

        return JsonResponse({
            'ticker': ticker,
            'dates': dates,
            'prices': prices,
            'news': news_list
        })
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

        return JsonResponse({
            'ticker': ticker,
            'dates': dates,
            'prices': prices,
            'news': news_list
        })
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
