
from data_shipper.main import CyberflyDataShipper
import time
key_pair = {"publicKey": "d04bbd8f403e583248aa461896bd7518113f89b85c98f3d9596bbfbf30df0bcb",
            "secretKey": "a0ec3175c6c80e60bc8ef18bd7b73a631c507b9f0a42c973036c7f96d21b047a"}

client = CyberflyDataShipper(device_id="test1", key_pair=key_pair, network_id="testnet04")


@client.on_message()
def do_something(data):
    print(data)


while 1:
    pass
