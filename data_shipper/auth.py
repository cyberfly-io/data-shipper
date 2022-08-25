from pypact.pact import Pact
from data_shipper import utils
import json
import time
from jsonschema import validate
from data_shipper import schema

pact = Pact()


def check_auth(cmd):
    try:
        validate(instance=cmd, schema=schema.pact_cmd_schema)
    except Exception as e:
        print(e.__str__())
        print("schema validation failed")
        return False
    pub_key = json.loads(cmd['cmd'])['signers'][0]['pubKey']
    verify = pact.crypto.verify(cmd['cmd'], pub_key, cmd['sigs'][0]['sig'])
    if verify:
        device = utils.read_device_json()
        if len(device.keys()) > 0 and pub_key in device['guard']['keys']:
            return True
        else:
            return False
    else:
        return False


def validate_expiry(msg):
    expiry_time = msg.get('expiry_time')
    if expiry_time:
        now = time.time().__round__()
        return now < expiry_time
    else:
        print("expiry_time required")
        return False
