import websocket
import json
from datetime import datetime, timedelta


class VWAP:

    def __init__(self):
        self.values_dict = {}
        self.start_time = datetime.now()

    def parse_message(self, message):
        for line in json.loads(message)['data']:
            price = line['p']
            volume = line['v']
            date = str(datetime.fromtimestamp(line['t'] / 1000).strftime('%Y-%m-%d %H:%M:%S'))
            dict_key = str(datetime.fromtimestamp(line['t'] / 1000).strftime('%Y-%m-%d %H:%M'))
            self.add_to_dict(self.values_dict, dict_key, price, volume)

            if datetime.now() - self.start_time >= timedelta(minutes=1.2):
                prev_key = str(self.start_time.strftime('%Y-%m-%d %H:%M'))
                print_out = self.values_dict.pop(prev_key)
                result = self.calculate_vwap(print_out['p'], print_out['v'], print_out['c'])
                print("-----------------------------------------------------")
                print(f"The VWAP for the previous minute period is: {result}")
                print("-----------------------------------------------------")
                start_time = datetime.now()

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


vwap = VWAP()
if __name__ == "__main__":
    vwap.run()
