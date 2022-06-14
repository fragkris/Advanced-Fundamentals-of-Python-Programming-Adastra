"""
- Task 1 completed and running properly.
- Task 2 Partly running. The formula should be fixed and late data should be considered. TODO
"""


import finnhub
import json
import websocket
from datetime import datetime

total_price = 0
total_volume = 0


def edit_message(message): #TODO can be optimized so it would only edit data but not print
    for line in json.loads(message)['data']:
        price = line['p']
        volume = line['v']
        calculate_vwap(price, volume)

        print(datetime.utcfromtimestamp(line['t'] / 1000).strftime('%Y-%m-%d %H:%M:%S'),
              "price:", line['p'],
              "volume:", line['v'])


def calculate_vwap(p, v):
    global total_price
    global total_volume

    total_price += p
    total_volume += v


def print_vwap():
    global total_price
    global total_volume

    print("Volume-weighted average price:", (total_price * total_volume)) #TODO Fix the formula
    total_price = 0
    total_volume = 0

def on_message(ws, message):
    edit_message(message)

    for data in json.loads(message)['data']:
        time = datetime.utcfromtimestamp(data['t'] / 1000).strftime('%Y-%m-%d %H:%M:%S')
        secs = str(time[-2:])

        if int(secs) == 00: #TODO consider late data
            print_vwap()


def on_close(ws):
    print("### closed ###")


def on_open(ws):
    ws.send('{"type":"subscribe","symbol":"BINANCE:BTCUSDT"}')


if __name__ == "__main__":
    websocket.enableTrace(False)
    ws = websocket.WebSocketApp("wss://ws.finnhub.io?token=cahkkgiad3i7auh49eb0",
                                on_message=on_message,
                                on_close=on_close)
    ws.on_open = on_open
    ws.run_forever()

