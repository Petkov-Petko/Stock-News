import requests
from twilio.rest import Client
STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"
twilio_sid = "YOUR TWILIO ACCOUNT SID"
twilio_auth = "YOUR TWILIO AUTH TOKEN"
STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
api_key = "YOUR OWN API KEY"
params = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK_NAME,
    "apikey": "YOUR OWN API KEY"
}

response = requests.get(url=STOCK_ENDPOINT, params=params)
response.raise_for_status()
a = response.json()
days = a["Time Series (Daily)"]

data_list = [value for (key, value) in days .items()]
yesterday = data_list[0]["4. close"]
day_before_yesterday = data_list[1]["4. close"]

diff = (float(yesterday) - float(day_before_yesterday))
up_or_down = None
if diff > 0:
    up_or_down ="⬆️"
else:
    up_or_down ="⬇️"
diff_percent = (diff / float(yesterday)) * 100

if abs(diff_percent) > 1:
    news_params = {
        "apikey": api_key,
        "q": STOCK_NAME
    }
    response_tesla = requests.get(url="https://newsapi.org/v2/everything?", params=news_params)
    response_tesla.raise_for_status()
    articles = (response_tesla.json()["articles"])
    three_articles = articles[:3]

    ready_for_send = [f"{STOCK_NAME}: {up_or_down}{diff_percent}%\nHeadline: {article['title']}. \nBrief: {article['description']}"for article in three_articles]
    client = Client(twilio_sid, twilio_auth)
    for article in ready_for_send:
        message = client.messages \
                        .create(
                             body=article,
                             from_='VIRTUAL_TWILIO_NUMBER',
                             to='VERIFIED_NUMBER'
                         )