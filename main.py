import requests
from twilio.rest import Client

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"


STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

STOCK_API_KEY = "JPXC7JCFZRNC2O17"
NEWS_API_KEY = "fbba1e61fe874449b70bcaf5bf42a1bf"
TWILIO_AUTH = "ACde43cbc8a7fbf1d59e3082f3d48a080a"
TWILIO_TOKEN = "ccbfcd290a1cbae2551783f679742ae5"

daily = []

para = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK_NAME,
    "apikey": STOCK_API_KEY

}
news_para = {
    "apiKey": NEWS_API_KEY,
    "qInTitle": COMPANY_NAME,
}

    ## STEP 1: Use https://www.alphavantage.co/documentation /#daily
# When stock price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").

response = requests.get(url=STOCK_ENDPOINT,params=para)
response.raise_for_status()
data = response.json()["Time Series (Daily)"]
data_list = [value for (key, value) in data.items()]
yesterday_data = data_list[0]
yesterday_closing = float(yesterday_data["4. close"])
print(yesterday_closing)


day_before_data = data_list[1]
day_before_closing = float(day_before_data["4. close"])
print(day_before_closing)


positive_differ = float(day_before_closing) - float(yesterday_closing)
up_down = "None"
if positive_differ > 0:
    up_down = "📈"
else:
    up_down = "📈"

differ_percent = (positive_differ / yesterday_closing) * 100
print(differ_percent)

#TODO 5. - If TODO4 percentage is greater than 5 then print("Get News").

if differ_percent >= 1:
    news = {}
    news_response = requests.get(url=NEWS_ENDPOINT, params=news_para)
    news_response.raise_for_status()
    news_data = news_response.json()["articles"][:3]
    news_dict = [f"Tesla: {up_down}{differ_percent}\nHeadline:{article['title']}. \nBrief:{article['description']}" for article in news_data]
    print(news_dict)

    client = Client(TWILIO_AUTH, TWILIO_TOKEN)
    for articles in news_dict:
        message = client.messages.create(
            body=articles,
            from_="+12562987331",
            to="+918108406735"
        )


#Optional TODO: Format the message like this: 
"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""

