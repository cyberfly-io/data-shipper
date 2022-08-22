# data-shipper
Device Python Client SDK beta

# Install

``pip install cyberfly-data-shipper``

# Usage


### Template 

```python
from data_shipper.main import CyberflyDataShipper
key_pair = {"publicKey": "your public key",
            "secretKey": "your secret key"}

client = CyberflyDataShipper(device_id="test", key_pair=key_pair)


@client.on_message()
def do_something(data):
    #print(data)
    pass

while 1:
    #send data
    pass
```


### Raspberry pi LED example
```python

from data_shipper.main import CyberflyDataShipper
import RPi.GPIO as GPIO
key_pair = {"publicKey": "d04bbd8f403e583248aa461896bd7518113f89b85c98f3d9596bbfbf30df0bcb",
            "secretKey": "a0ec3175c6c80e60bc8ef18bd7b73a631c507b9f0a42c973036c7f96d21b047a"}

client = CyberflyDataShipper(device_id="your device id from io platform", key_pair=key_pair)

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)


@client.on_message()
def do_something(data):
    pin_no = data.get("pin_no")
    state = data.get("state")
    GPIO.setup(pin_no, GPIO.OUT)
    if state:
       GPIO.output(pin_no, GPIO.HIGH)
    else:
        GPIO.output(pin_no, GPIO.LOW)

while 1:
    pass
```