#https://pypi.org/project/websocket_client/
import time
import websocket
import json
from datetime import datetime, timedelta
import numpy as np
import asyncio

TOTAL_PRICE = 0
TOTAL_VOLUME = 0
VALUES_DICT = {}
START_TIMER = 0
PREV_MINUTE = 0


def edit_message(message):
    global VALUES_DICT
    global PREV_MINUTE
    global TOTAL_VOLUME
    global TOTAL_PRICE
    for line in json.loads(message)['data']:
        price = line['p']
        volume = line['v']
        calculate_vwap(price, volume)
        date = str(datetime.utcfromtimestamp(line['t'] / 1000).strftime('%Y-%m-%d %H:%M:%S'))
        dict_date = str(datetime.utcfromtimestamp(line['t'] / 1000).strftime('%Y-%m-%d %H:%M'))
        secs = str(date[-2:])
        PREV_MINUTE = int(datetime.utcfromtimestamp(line['t'] / 1000).strftime('%M')) - 1
        VALUES_DICT[dict_date] = get_vwap()

        return "{}, price: {}, volume: {}".format(date, price, volume)



def calculate_vwap(p, v):
    global TOTAL_PRICE
    global TOTAL_VOLUME

    TOTAL_PRICE += p
    TOTAL_VOLUME += v


def get_vwap():
    global TOTAL_PRICE
    global TOTAL_VOLUME
    return np.cumsum(TOTAL_PRICE * TOTAL_VOLUME) / np.cumsum(TOTAL_PRICE)
    # TOTAL_PRICE = 0
    # TOTAL_VOLUME = 0


def on_message(ws, message):
    global VALUES_DICT
    print(edit_message(message))





def on_close(ws):
    print("### closed ###")


def on_open(ws):
    ws.send('{"type":"subscribe","symbol":"BINANCE:BTCUSDT"}')


if __name__ == "__main__":
    websocket.enableTrace(False)
    ws = websocket.WebSocketApp( "wss://ws.finnhub.io?token=cahkkgiad3i7auh49eb0" ,
                              on_message = on_message,
                              on_close = on_close)
    ws.on_open = on_open
    ws.run_forever()
