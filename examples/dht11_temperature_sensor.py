import adafruit_dht
import board
from data_shipper.main import CyberflyDataShipper
dht = adafruit_dht.DHT11(board.D4)
key_pair = {"publicKey": "d04bbd8f403e583248aa461896bd7518113f89b85c98f3d9596bbfbf30df0bcb",
            "secretKey": "a0ec3175c6c80e60bc8ef18bd7b73a631c507b9f0a42c973036c7f96d21b047a"}

client = CyberflyDataShipper(device_id="d843cbb5-94e9-4cd7-9ea0-c8339b11b440", key_pair=key_pair, network_id="testnet04")


@client.on_message()
def do_something(data):
    print(data)
    data_var = data.get('dataVar')
    if data_var == "temp":  # data variable you define in widget
        temperature = dht.temperature
        client.publish(data.get('response_topic'), {data_var: temperature})


while 1:
    pass
