import pyupbit
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timedelta
import time
import warnings

# 경고 메시지 숨기기
warnings.filterwarnings('ignore')

# 한글 폰트 설정
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['axes.unicode_minus'] = "False"

import requests
def get_current_prices_api(tickers):
    """
    업비트 API를 사용하여 여러 암호화폐의 현재가를 조회하는 함수

    Args:
        tickers (list): 조회할 암호화폐 티커 리스트

    Returns:
        dict: {티커: 현재가} 형태의 딕셔너리
    """
    url = "https://api.upbit.com/v1/ticker"
    headers = {"accept": "application/json"}

    # 여러 티커를 쉼표로 연결
    markets_param = ",".join(tickers)
    params = {"markets": markets_param}

    print(f">>>>>>>>>>> prameters: {params}")  # API 요청에 사용되는 파라미터 출력
    # API 요청
    response = requests.get(url, headers=headers, params=params)
    prices_data = response.json()

    # 딕셔너리 형태로 변환
    prices = {}
    for data in prices_data:
        prices[data['market']] = data['trade_price']

    return prices

print(get_current_prices_api(["KRW-BTC"]))
pyupbit.get_current_price(["KRW-BTC"])

class UpbitDataCollector:
    """Upbit API를 활용한 데이터 수집 클래스"""

    def __init__(self):
        self.supported_tickers = None

    def get_krw_tickers(self):
        """KRW 마켓의 모든 티커 조회"""
        try:
            tickers = pyupbit.get_tickers(fiat="KRW")
            self.supported_tickers = tickers
            return tickers
        except Exception as e:
            print(f"티커 조회 오류: {e}")
            return []

    def get_current_prices(self, tickers):
        """현재가 조회"""
        try:
            if isinstance(tickers, str):
                return pyupbit.get_current_price(tickers)
            else:
                return pyupbit.get_current_price(tickers)
        except Exception as e:
            print(f"현재가 조회 오류: {e}")
            return None

    def get_ohlcv_data(self, ticker, interval="day", count=30):
        """OHLCV 데이터 조회"""
        try:
            df = pyupbit.get_ohlcv(ticker, interval=interval, count=count)
            if df is not None:
                df['ticker'] = ticker
                df.reset_index(inplace=True)
            return df
        except Exception as e:
            print(f"{ticker} OHLCV 데이터 조회 오류: {e}")
            return None
            # -----------| ---------|----------
            # ticker         df.data   df.data
    def get_multiple_ohlcv(self, tickers, interval="day", count=30, delay=0.1):
        """여러 티커의 OHLCV 데이터 일괄 조회"""
        all_data = []

        for ticker in tickers:
            print(f"{ticker} 데이터 수집 중...")
            data = self.get_ohlcv_data(ticker, interval, count)
            if data is not None:
                all_data.append(data)
            time.sleep(delay)  # API 호출 제한 고려

        if all_data:
            return pd.concat(all_data, ignore_index=True)
        return pd.DataFrame()

# 클래스 인스턴스 생성
collector = UpbitDataCollector()

# 1. str  "122220000"
# 2. dict {"KRW-BTC":"12002222"}
print(collector.get_current_prices("KRW-BTC"))
print(collector.get_current_prices(["KRW-BTC", "KRW-ETH"])) 

major_tickers = "KRW-BTC" #["KRW-BTC","KRW-ETC","KRW-XRP"]

# 현재가 조회
current_prices = collector.get_current_prices(major_tickers)
current_prices

major_tickers = ["KRW-BTC","KRW-ETC","KRW-XRP"]


# ===========================
#  문제1 구현
# ===========================

def collect_market_data():
    print("===[collect_market_data] 현재가 조회 ====")
    current_prices = collector.get_current_prices(major_tickers)
    print(current_prices)

    print("\n====[collect_market_data] OHLCV 데이터 조회 ====")
    raw_data = collector.get_multiple_ohlcv(
        tickers=major_tickers,
        interval="day",
        count=30
    )

    print(raw_data.head())
    print("\n데이터 개수:", len(raw_data))

    return current_prices, raw_data

current_prices, raw_data = collect_market_data()

# ===========================
#  문제1 구현 end
# ===========================


# 수집된 데이터 미리보기
print(f"\n데이터 형태: {raw_data.shape}")
print(f"\n데이터 타입:\n{raw_data.dtypes}")

raw_data.head(10)

df = raw_data.head(5)
df
print(df)

raw_data


# ===========================
#  ticker	KRW-BTC	KRW-BTC, KRW-ETC, KRW-XRP
# ===========================

key = raw_data.groupby('ticker')
print("그룹 키:>>>>>>>>>>>>>>>>>>")
print(key.groups.keys())
print("그룹 값:>>>>>>>>>>>>>>>>>>")
print(key.groups.values())


for ticker, each_df in raw_data.groupby('ticker'):
    print("\n====================")
    print(ticker)
    print("====================")
    print(each_df.head(2).to_string(index=False))


def preprocess_data(df):
    """데이터 전처리 함수"""
    print("=== 데이터 전처리 시작 ===")

    # 1. 데이터 복사
    processed_df = df.copy()

    # 2. 날짜 컬럼 처리
    if 'index' in processed_df.columns:
        processed_df['date'] = pd.to_datetime(processed_df['index'])
        processed_df.drop('index', axis=1, inplace=True)

    # 정렬 
    processed_df = processed_df.sort_values(by=["ticker", "date"])

    # 3. 문자열 날짜 컬럼 (DB 저장용)
    processed_df['date_str'] = processed_df['date'].dt.strftime('%Y-%m-%d %H:%M:%S')

    ##############################################################
    # 문제1
    ##############################################################

    # 종가 - 시가
    processed_df['price_change'] = processed_df['close'] - processed_df['open']

    # 변동률 (%)
    processed_df['price_change_pct'] = (processed_df['price_change'] / processed_df['open']) * 100

    # 고가 - 저가
    processed_df['high_low_diff'] = processed_df['high'] - processed_df['low']

    ##############################################################
    # 문제2
    ##############################################################

    # 티커별 5일 이동평균
    processed_df['ma5'] = processed_df.groupby('ticker')['close'].transform(
        lambda x: x.rolling(window=5, min_periods=1).mean()
    )

    # 결측치 → 종가로 대체
    processed_df['ma5'] = processed_df['ma5'].fillna(processed_df['close'])

    ##############################################################

    # 4. 컬럼 순서 정리
    columns_order = [
        'date', 'date_str', 'ticker',
        'open', 'high', 'low', 'close', 'volume',
        'price_change', 'price_change_pct', 'high_low_diff', 'ma5'
    ]

    processed_df = processed_df[columns_order]

    print(f"전처리 완료 - 행 수: {len(processed_df)}")
    print("추가된 컬럼: price_change, price_change_pct, high_low_diff, ma5")

    # 미리보기 출력
    print("\n==== 전처리 결과 미리보기 ====")
    print(processed_df.head(10).to_string(index=False))

    return processed_df


processed_data = preprocess_data(raw_data)

print("============ df 확인 =============")
print(df)

#processed_data.to_csv("processed_market_data.csv", index=False, encoding="utf-8-sig")
#print("============= CSV 저장 완료 ======== ")
