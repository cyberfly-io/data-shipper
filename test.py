
from data_shipper.main import CyberflyDataShipper
import time
key_pair = {"publicKey":"29f864a5e8eb8e926a9a933e9663556e031bdb4e40d4e365b7bac03a7bd3f265",
            "secretKey":"7c7158f0f9b0c75a858cb04c8854d7411d889ca1a6dd00c6044258544f24bd89"}

client = CyberflyDataShipper(device_id="4af0969b-fefd-4f46-b2fe-3a43158ab00c", key_pair=key_pair, network_id="testnet04")

import random


@client.on_message()
def do_something(data):
    print(data)
    data_var = data.get('dataVar')
    if data_var == "temp":
        client.publish(data.get('response_topic'), {data_var: random.randint(30, 40)})
    elif data_var == "water":
        client.publish(data.get('response_topic'), {data_var: random.randint(50, 70)})
    elif data_var == 'location':
        client.publish(data.get('response_topic'), {data_var: randlatlon()})


def randlatlon():
    return (round(random.uniform(-90,  90), 5),
            round(random.uniform(-180, 180), 5))


while 1:
    client.store_data({"temperature": random.randint(20, 40)})
    time.sleep(3)
    pass
