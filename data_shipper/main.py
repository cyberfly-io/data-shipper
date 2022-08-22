import json
import time

import pypact.utils
import requests
from pypact.pact import Pact
from typing import Callable
import paho.mqtt.client as mqtt

from data_shipper import config, utils, auth

mqttc = mqtt.Client(clean_session=True)


class CyberflyDataShipper:
    def __init__(self, device_id: str, key_pair: dict, network_id: str = "mainnet01"):
        self.key_pair = key_pair
        self.network_id = network_id
        self.api_host = config.api_host
        self.device_data = {}
        self.device_id = device_id
        self.account = "k:" + self.key_pair.get("publicKey")
        self.caller = default_caller
        self.mqtt_client = mqttc
        self.topic = device_id
        self.mqtt_client.user_data_set(self)
        self.mqtt_client.on_connect = on_connect
        self.mqtt_client.on_message = on_received
        self.run(config.mqtt_broker, config.mqtt_port)

    def update_data(self, key: str, value):
        self.device_data.update({key: value})

    def send_data(self, store_data=False):
        pact = Pact()
        self.device_data.update({"timestamp": time.time().__round__()})
        hsh = utils.get_data_hash(self.device_data)
        code = pact.lang.mk_exp(module_and_function="cyberfly_devices.new-device-data", namespace="free", id=hsh,
                                data="(read-msg 'deviceData)", device_id=self.device_id)
        data = {
            "ks": {"pred": "keys-all", "keys": [self.key_pair['publicKey']]},
            "deviceData": json.dumps(self.device_data)
        }

        kp = self.key_pair
        cmd = {
            "pactCode": code,
            "envData": data,
            "meta": utils.default_meta(self.account),
            "networkId": self.network_id,
            "nonce": time.time().__round__()-15,
            "keyPairs": [kp]
        }
        signed_message = pact.fetch.make_prepare_cmd(cmd)
        final_cmd = pact.api.mk_public_send(signed_message)
        final_cmd.update({"store_data": store_data, "device_id": self.device_id})
        try:
            res = requests.post(config.api_host, json=final_cmd)
            return pypact.utils.parse_res(res)
        except Exception as e:
            print(e.__str__())

    def on_message(self) -> Callable:
        def decorator(callback_function):
            self.caller = callback_function

        return decorator

    def run(self, host: str, port: int) -> None:
        self.mqtt_client.connect(
            host, port, 60
        )
        self.mqtt_client.loop_start()


def on_connect(client: mqtt.Client, mqtt_class: CyberflyDataShipper, __flags, received_code: int) -> None:
    print("Connected with result code " + str(received_code))
    client.subscribe(mqtt_class.topic)


def on_received(__client: mqtt.Client, mqtt_class: CyberflyDataShipper, msg: mqtt.MQTTMessage) -> None:
    json_string = msg.payload.decode("utf-8")
    try:
        json_data = json.loads(json_string)
        if auth.validate_device_id(mqtt_class.device_id, json_data) and auth.check_auth(json_data):
            try:
                mqtt_class.caller(json.loads(json_data['cmd'])['payload']['exec']['data']['device_exec'])
            except Exception as e:
                print(e.__str__())
    except Exception as e:
        print("invalid json payload received")


def default_caller(data):
    pass
