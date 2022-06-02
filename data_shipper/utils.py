import hashlib
import json
import time
from pypact.pact import Pact


def get_data_hash(data):

    return hashlib.sha256(json.dumps(data).encode('utf-8')).hexdigest()


def default_meta():
    pact = Pact()
    return pact.lang.mk_meta("cyberfly-gas-station", "1", 0.0000001, 3000, time.time().__round__()-15, 28800)
