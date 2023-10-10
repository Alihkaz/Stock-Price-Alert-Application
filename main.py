#


import requests
from twilio.rest import Client
from twilio.http.http_client import TwilioHttpClient




STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"


STOCK_ENDPOINT = "https://www.alphavantage.co/query"


NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
api_key=  "539fff1b9576454f9e0dd45c5f7cd2ed"


account_sid = "YOUR ACCOUNT SID"#get them from twilio 
auth_token = "AUTH_TOKEN"



price_params = {

    
    "function" : "TIME_SERIES_INTRADAY",#here we used the intra day because the daily is premium ! 
    "symbol": STOCK,
    "interval":"60min",  
    "outputsize":"compact",
    "apikey": "4OZSPRTH0XVNS41S",
    
}




price_response = requests.get(STOCK_ENDPOINT, params=price_params)
price_response.raise_for_status()
price_data = price_response.json()

closing_price_of_yesterday=float(price_data["Time Series (60min)"]["2023-05-17 12:00:00"]["4. close"])



closing_price_of_before_yesterday=float(price_data["Time Series (60min)"]["2023-05-16 12:00:00"]["4. close"])#here the dictionaries and the keys are nisted, we provide the path through watching the test from the api 


up_down=None
price_difference=(closing_price_of_yesterday)-((closing_price_of_before_yesterday))
if price_difference>0:
  up_down= "▲"
else:
  up_down="▼"



difference_percentage = float(100*(price_difference))/closing_price_of_before_yesterday

if 0<difference_percentage<5 or difference_percentage<-5 :






  news_params = {
    
      "qInTitle": COMPANY_NAME ,
      "apiKey": api_key,
     
      
  }
  
  
  news_response = requests.get(NEWS_ENDPOINT, params=news_params)
  news_response.raise_for_status()
  news_data = news_response.json()["articles"]
  news_data_slice = news_data[:3]

  # print(news_data_slice)




#sending SMS :


  news_list=[(f"headline: {item['title']} \n Brief: {item['description']}") for item in news_data_slice] 
  
   
  
  client = Client(account_sid, auth_token)
  for item in news_list:

    message = client.messages \
          .create(
          body=f"{COMPANY_NAME}{up_down}{difference_percentage}%\n{item}",
          from_="YOUR TWILIO VIRTUAL NUMBER",
          to="YOUR TWILIO VERIFIED REAL NUMBER"
      )
    print(message.status)
  




