from datetime import date,timedelta
import requests as rq
import os
from messaging import send_msg
from twilio.rest import Client
STOCK = "TSLA"
DIRECTION = ""
COMPANY_NAME = "Tesla Inc"
STOCKS_ENDP = "https://www.alphavantage.co/query"
NEWS_ENDP = " https://newsapi.org/v2/everything"
ACC_SID = os.environ.get('ACCOUNT_SID')
AUTH_KEY = os.environ.get('AUTHENTICATION_KEY')
MY_MOBILE = os.environ.get('MY_MOB_NO')
TODAY = date.today()
YESTERDAY = (TODAY - timedelta(days=1)).strftime("%Y-%m-%d")
ERE_YESTERDAY = (TODAY - timedelta(days=2)).strftime("%Y-%m-%d")
STOCK_KEY = os.environ.get('SE_API_KEY')
NEWS_API_KEY = os.environ.get('NEWS_KEY')
NEWS_ARTICLES = []
CURRATED_NEWS = []
stocks_param = {
    "function":"TIME_SERIES_DAILY",
    "symbol":STOCK,
    "outputsize":"compact",
    "datatype":"json",
    "apikey":STOCK_KEY
}
news_param ={
    "q":STOCK and COMPANY_NAME,
    "searchIn":"title,content",
    "domains":"marketwatch.com",
    "from": ERE_YESTERDAY,
    "to": YESTERDAY,
    "sortBy":"relevancy",
    "apiKey":NEWS_API_KEY,
}


# difference % original x 100


## STEP 1: Use https://www.alphavantage.com
# When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").
stocks_response = rq.get(url=STOCKS_ENDP , params=stocks_param)
stocks_response.raise_for_status()
stocks_data = stocks_response.json()["Time Series (Daily)"]
data_list = [values for (key, values) in stocks_data.items()]
print(data_list)
yesterday_closing = float(data_list[0]["4. close"])
ere_yesterday_closing = float(data_list[1]["4. close"])
# yesterday_closing = 120.34
# ere_yesterday_closing = 160.30
dif = yesterday_closing - ere_yesterday_closing
if dif > 0:
    DIRECTION = "🔺"
else:
    DIRECTION = "🔻"
change = abs(round(dif / ere_yesterday_closing * 100, 2))
get_news = False
if change >= 5.0:
    get_news = True
print(change)

## STEP 2: Use https://newsapi.org
# Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME.
if get_news:
    news_response = rq.get(url=NEWS_ENDP, params=news_param)
    news_data = news_response.json()['articles']
    TOP_NEWS = news_data[:3]
    formatted_news = [f"{STOCK}:{DIRECTION}{change}+%\n Headline:{news['title']}\n Brief:{news['description']}" for news in TOP_NEWS ]


if get_news:
   send_msg(formatted_news)


## STEP 3: Use https://www.twilio.com
# Send a seperate message with the percentage change and each article's title and description to your phone number.
# def send_news(article_list):
#     for n in range(len(article_list)):
#         client = Client(ACC_SID, AUTH_KEY)
#         message = client.messages \
#             .create(
#                 body=f"TSLA:{article_list[n]['TSLA']}\
#                      Headline:{article_list[n]['Headline']}\
#                      Brief: {article_list[n]['Brief']}",
#
#                 from_="+18285481059",
#                 to=MY_MOBILE
#             )



#Optional: Format the SMS message like this: 
"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""

