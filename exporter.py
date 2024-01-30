# Buffaloのルータの管理画面からパケット数のページへアクセスし、Cloudwatch へPutMetricする。後はグラフ化するなりダッシュボード化するなり色々
# 管理画面のURLは下記に指定

from bs4 import BeautifulSoup
import re
from pprint import pprint
import requests
import boto3
import datetime

def send_metrics(name,val):
    region = 'us-east-1'
    cloudwatch = boto3.client('cloudwatch', region_name=region)
    metric_data = [
        {
            'MetricName': name,
            'Dimensions': [],
            'Timestamp': datetime.datetime.utcnow(),
            'Value': int(val),
            'Unit': 'Count'  # メトリクスの単位を指定
        },
    ]
    response = cloudwatch.put_metric_data(
        Namespace="home-lan",
        MetricData=metric_data
    )
    print("PutMetricData Response:", response)

def extract_numbers_from_table():
    # BeautifulSoupを使用してHTMLを解析
    #response = requests.get("https://tomita.s3.ap-northeast-1.amazonaws.com/packet.html")
    url = "http://localhost:8888/packet.html"
    response = requests.get(url)
    response.raise_for_status()
    source_encoding = response.encoding
    html = response.content.decode(source_encoding).encode("utf-8").decode("utf-8")

    soup = BeautifulSoup(html, 'html.parser')

    tds = soup.find_all('td')

    td_texts = [td.get_text(strip=True) for td in tds]
    pprint(td_texts)
    send_metrics('wan-out',td_texts[0])
    send_metrics('wan-in',td_texts[2])
    send_metrics('lan-out-wired',td_texts[4])
    send_metrics('lan-in-wired',td_texts[6])
    send_metrics('lan-out-wireless2.4g',td_texts[8])
    send_metrics('lan-in-wireless2.4g',td_texts[10])
    send_metrics('lan-out-wireless5g',td_texts[12])
    send_metrics('lan-in-wireless5g',td_texts[14])


# テーブルから数値を抽出
extract_numbers_from_table()






