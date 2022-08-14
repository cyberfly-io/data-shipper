from pypact.pact import Pact
from data_shipper import utils
import time
key_pair = {"publicKey": "d04bbd8f403e583248aa461896bd7518113f89b85c98f3d9596bbfbf30df0bcb",
            "secretKey": "a0ec3175c6c80e60bc8ef18bd7b73a631c507b9f0a42c973036c7f96d21b047a"}

pact = Pact()
code = pact.lang.mk_exp(module_and_function="sensor_store6.new-device", namespace="free", device_id="test12345",
                        name="test12345 device", status="active", ks="(read-keyset 'ks)")
data = {
    "ks": {"pred": "keys-any", "keys": [key_pair['publicKey'], 'f03fb771f7727797291d877e5085803c84e72d06563a6dc704453dde404fca79']},
}

cmd = {
    "pactCode": code,
    "envData": data,
    "meta": utils.default_meta(sender="k:"+key_pair['publicKey']),
    "networkId": "testnet04",
    "nonce": time.time().__round__() - 15,
    "keyPairs": [key_pair]
}

print(pact.fetch.send(cmd, "https://api.testnet.chainweb.com/chainweb/0.0/testnet04/chain/1/pact"))
