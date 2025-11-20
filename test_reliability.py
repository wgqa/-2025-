# file: test_reliability.py
import time, requests

def test_reliability():
    start = time.time()
    for i in range(1000):
        res = requests.post("http://127.0.0.1:5000/order",
                            json={"item": "book", "qty": 1})
        assert res.status_code == 200 or res.status_code == 400
    end = time.time()
    print("运行时长：", end - start, "秒")