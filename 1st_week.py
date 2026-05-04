
import requests
from datetime import datetime
import time
import json

#url = "https://api.upbit.com/v1/market/all"
#headers = {"accept": "application/json"}
#response = requests.get(url, headers=headers)
#print(response)
#all_markets = response.json()
#print(all_markets)

#tickers = ["KRW-BTC", "KRW-ETH", "KRW-XRP", "KRW-SOL"]
#현재가 조회 함수 작성
def get_current_prices_api(tickers):

    print(f'get_current_prices_api enter tickers == {tickers}')
    url = "https://api.upbit.com/v1/ticker"
    headers = {"accept": "application/json"}

    markets_param   = ",".join(tickers)             #tickers 리스트를 ',' 로 구분자로 하여 하나의 문자열로 합치기
    params          = {"markets": markets_param}    #사용할 parameter 
    #print(f"params ===> {params}")
    response        = requests.get(url, headers=headers, params=params) #api로 통신하여 값 조회
    prices_data     = response.json()                                   #조회값 json으로 formatting

    ##json 데이터 출력 
    #print(f"prices_data : {prices_data}")

    #코인별 현재가 출력
    trade_price = {}
    for price_data in prices_data:
        trade_price[price_data['market']] = price_data['trade_price']
    #print('trade_price == ',trade_price)
    return trade_price


#포트폴리오 분석 함수
portfolio = {
    "KRW-BTC"   : 0.1,
    "KRW-ETH"    : 3 ,
    "KRW-XRP"   : 1000
   # ,"KRW-SOL"   : 10
}
def analyze_portfolio(portfolio) : 
    tickers = list(portfolio.keys())
    #print('tickers => ',tickers)
    #1.현재가 조회
    prices = get_current_prices_api(tickers)
    print(f'prices ==> {prices}')
    #2.각 암호화폐별 분석  
    # - 현재가 × 보유 수량 → 개별 가치 계산
    # - `portfolio_analysis` 리스트에 코인명, 수량, 현재가, 가치 저장
    # - 동시에 `total_value`(총합)를 누적
    

    portfolio_analysis  = []
    total_value         = 0 

    for ticker, quantity in portfolio.items():
        if ticker in prices:
            current_price = prices[ticker]
            value = current_price * quantity #현재가 × 보유 수량 → 개별 가치 계산
            total_value += value #총합 누적
            portfolio_analysis.append({
                "코인": ticker.split('-')[1],  # 'KRW-BTC' -> 'BTC' 
                "수량": quantity,
                "현재가": current_price,
                "가치": value
            })
    #3.비중계산
    for item in portfolio_analysis:
        item['비중'] = (item['가치'] / total_value) * 100 
    
    # print("="*80)
    # print("포트폴리오 분석 결과")
    # print("="*80)
    # print(f"\n총 포트폴리오 가치: {total_value:,.0f}원\n")
    # print("-"*80)
    # print(f"{'코인':^10} {'수량':>15} {'현재가':>18} {'가치':>18} {'비중':>12}")
    # print("-"*80)

    return portfolio_analysis

print('analyze_portfolio >> ', analyze_portfolio(portfolio))


