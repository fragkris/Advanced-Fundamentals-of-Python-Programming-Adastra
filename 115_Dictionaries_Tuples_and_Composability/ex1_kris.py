"""
The program streams bitcoin price in real time. Few seconds after every minute passed, the
program calculates and prints VWAP for the previous minute.
It is possible that the program collects and never deletes some late data, if It arrives after the given
1.2 minutes.
However, this is very unlikely in this scenario.
Since the program is mostly for demonstration, I didn't bother implementing a cleaning code for
unused information.
"""

import websocket
import json
from datetime import datetime, timedelta


class StreamPricesAndVWAP:

    def __init__(self):
        self._values_dict = {}
        self._start_time = datetime.now()

    def parse_message(self, message):
        for line in json.loads(message)['data']:
            price = line['p']
            volume = line['v']
            date = str(datetime.fromtimestamp(line['t'] / 1000).strftime('%Y-%m-%d %H:%M:%S'))
            dict_key = str(datetime.fromtimestamp(line['t'] / 1000).strftime('%Y-%m-%d %H:%M'))
            self.add_to_dict(self._values_dict, dict_key, price, volume)

            if datetime.now() - self._start_time >= timedelta(minutes=1.2):
                prev_key = str(self._start_time.strftime('%Y-%m-%d %H:%M'))
                print_out = self._values_dict.pop(prev_key)
                result = self.calculate_vwap(print_out['p'], print_out['v'], print_out['c'])
                print("-----------------------------------------------------")
                print(f"The VWAP for the previous minute period is: {result}")
                print("-----------------------------------------------------")
                self._start_time = datetime.now()

            return "{}, price: {}, volume: {}".format(date, price, volume)

    def add_to_dict(self, dictry, key, price, volume):
        if key not in dictry:
            dictry[key] = {"p": price, "v": volume, "c": 1}
        else:
            dictry[key] = {"p": dictry.get(key)['p'] + price,
                           "v": dictry.get(key)['v'] + volume,
                           "c": dictry.get(key)['c'] + 1}

    def calculate_vwap(self, p, v, c):
        return round(((p * v) / c) / (v * c), 2)

    def on_message(self, ws, message):
        print(self.parse_message(message))

    def on_close(self, ws):
        print("### closed ###")

    def on_open(self, ws):
        ws.send('{"type":"subscribe","symbol":"BINANCE:BTCUSDT"}')

    def run(self):
        websocket.enableTrace(False)
        ws = websocket.WebSocketApp("wss://ws.finnhub.io?token=cahkkgiad3i7auh49eb0",
                                    on_message=self.on_message,
                                    on_close=self.on_close)
        ws.on_open = self.on_open
        ws.run_forever()


spav = StreamPricesAndVWAP()
if __name__ == "__main__":
    spav.run()
