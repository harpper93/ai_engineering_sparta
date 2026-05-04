
import requests

#url = "https://api.upbit.com/v1/market/all"
#headers = {"accept": "application/json"}
#response = requests.get(url, headers=headers)
#print(response)
#all_markets = response.json()
#print(all_markets)

tickers = ["KRW-BTC", "KRW-ETH", "KRW-XRP", "KRW-SOL"]
#현재가 조회 함수 작성
def get_current_prices_api(tickers):

    url = "https://api.upbit.com/v1/ticker"
    headers = {"accept": "application/json"}

    markets_param   = ",".join(tickers)             #tickers 리스트를 ',' 로 구분자로 하여 하나의 문자열로 합치기
    params          = {"markets": markets_param}    #사용할 parameter 

    response        = requests.get(url, headers=headers, params=params) #api로 통신하여 값 조회
    prices_data     = response.json()                                   #조회값 json으로 formatting

    #print(f"prices_data : {prices_data}")

    #코인별 현재가 출력
    trade_price = {}
    for data in trade_price:
        trade_price[data['market']] = data['trade_price']

    return trade_price


#포트폴리오 분석 함수
portfolio = {
    "KRW-BTC" : 0.1,
    "KRW-EH" : 3 ,
    "KRX-XRP" : 1000
}
def analyze_portfolio(portfolio) : 
    tickers = list(portfolio.keys())
    return null

print('analyze_portfolio >> ', analyze_portfolio(tickers))
