# file: test_sql_injection.py
import requests

def test_sql_injection():
    url = "http://127.0.0.1:5000/login"
    # 经典 SQL 注入 payload
    payload = {"username": "' OR 1=1--", "password": "xxx"}
    res = requests.post(url, json=payload)

    # 期望：服务器拒绝或返回错误信息
    assert res.status_code == 400 or "error" in res.text.lower()