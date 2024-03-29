from pypact.pact import Pact
from data_shipper import config, utils
import time
from bigchaindb_driver import BigchainDB
bdb_root_url = 'http://170.187.249.181:9984/'  # Replace with your BigchainDB node URL
bdb = BigchainDB(bdb_root_url)


def get_rules(device_id: str, network_id: str, key_pair: dict) -> list:
    pact = Pact()
    pact_code = '({}.{}.read-device-rules "{}")'.format(config.namespace, config.module, device_id)
    cmd = {
        "pactCode": pact_code,
        "envData": {},
        "meta": utils.default_meta(),
        "networkId": network_id,
        "nonce": time.time().__round__() - 15,
        "keyPairs": [key_pair]
    }
    try:
        rules = pact.fetch.local(cmd, utils.get_api_host(network_id))
        if isinstance(rules, dict) and rules.get('result')['status'] == "success":
            return rules.get('result')['data']
        else:
            return []
    except Exception as e:
        print(e.__str__())
        return []


def get_device(device_id: str, network_id: str, key_pair: dict) -> dict:
    conn = False
    while not conn:
        if utils.is_cnx_active() is True:
            conn = True
            pact = Pact()
            pact_code = '({}.{}.get-device "{}")'.format(config.namespace, config.module, device_id)
            cmd = {
                "pactCode": pact_code,
                "envData": {},
                "meta": utils.default_meta(),
                "networkId": network_id,
                "nonce": time.time().__round__() - 15,
                "keyPairs": [key_pair]
            }
            try:
                devices = pact.fetch.local(cmd, utils.get_api_host(network_id))
                if isinstance(devices, dict) and devices.get('result')['status'] == "success":
                    return devices.get('result')['data']
                else:
                    return {}
            except Exception as e:
                print(e.__str__())
                return {}
        else:
            print("no internet")


def store_data(data, keypair):
    # Create a transaction
    tx = bdb.transactions.prepare(
        operation='CREATE',
        signers=keypair['publicKey'],
        asset={'data': data}
    )

    # Sign and submit the transaction
    signed_tx = bdb.transactions.fulfill(
        tx,
        private_keys=keypair['secretKey']
    )
    try:
        bdb.transactions.send_commit(signed_tx)
    except Exception as e:
        print(e)
