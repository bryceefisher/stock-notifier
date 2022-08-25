import requests
from twilio.rest import Client

# Constants
STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"
STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
NEWS_API_KEY = "Your newsapi.org API key"
STOCK_API_KEY = "Your alphavantage.co api key"
ACCOUNT_SID = "twilio SID"
AUTH_TOKEN = 'Twilio auth token'
CLIENT = Client(ACCOUNT_SID, AUTH_TOKEN)

# Api Parameters
news_params = {
    "q": STOCK,
    "apiKey": NEWS_API_KEY
}

stock_params = {
    "function": "TIME_SERIES_INTRADAY",
    "symbol": STOCK,
    "apikey": STOCK_API_KEY,
    "interval": "60min",
    "adjusted": "false"
}

# Receive stock data from https://www.alphavantage.co/query
stock_response = requests.get(STOCK_ENDPOINT, stock_params)
stock_data = stock_response.json()

# Filter most recent stock close price
recent_stock_pull = list(stock_response.json()['Time Series (60min)'])[0]
current_close = float(stock_data['Time Series (60min)'][recent_stock_pull]["4. close"])

# Filter most 24hr ago stock close price
day_old_stock_pull = list(stock_response.json()['Time Series (60min)'])[23]
yesterday_close = float(stock_data['Time Series (60min)'][day_old_stock_pull]["4. close"])

# Determine 5% of yesterday's close price
five_percent = yesterday_close * .05

# Retrieve absolute value of difference between today and yesterday's value

difference = abs(yesterday_close - current_close)

# retrieve value that will be used to determine whether arrow points up or down
arrow_difference = yesterday_close - current_close

# Movement percentage expressed as whole number
daily_movement = int(round((difference / yesterday_close), 2) * 100)

# Determine whether arrow points up or down
if difference > 0:
    arrow = "⬆️"
else:
    arrow = "⬇️"

# Determine whether movement is 5% or more and if so send 3 most recent news article pertaining to stock
if difference >= five_percent:
    news_response = requests.get(NEWS_ENDPOINT, params=news_params)
    news_data = news_response.json()
    for article in news_data["articles"][:3]:
        message = CLIENT.messages.create(
            body=f"TSLA: {arrow} {daily_movement}%\nHeadline: {article['title']}\nArticle: {article['url']}",
            from_='Your Twilio ph#',
            to='ph# to receive text'
        )
