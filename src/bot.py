import json
import time
import requests
import datetime
import threading

i = 0


def send_neat_request():
    global i
    i = i + 1
    get_data = {
        "server": "199",
        "player": "jigar",
        "city": "ahm",
        "time": datetime.datetime.now().timestamp()
    }
    gr = requests.get('http://localhost:8888/neat', params=get_data)
    command = gr.text
    post_data = {"account": get_data, "return": "OKAY"}
    post_data["return"] = {
        "catapult": "abc",
        "carriage": "A2222S",
        "batteringRam": 123,
        "id": i,
        "command": command
    }
    time.sleep(2)
    pr = requests.post(
        'http://localhost:8888/neat', data=json.dumps(post_data))
    threading.Timer(3, send_neat_request).start()


if __name__ == "__main__":
    send_neat_request()