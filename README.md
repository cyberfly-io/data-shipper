# data-shipper
Device Python Client SDK
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


### Raspberry pi LED and sent temperature data sent example
```python

from data_shipper.main import CyberflyDataShipper
import time
import RPi.GPIO as GPIO
key_pair = {"publicKey": "d04bbd8f403e583248aa461896bd7518113f89b85c98f3d9596bbfbf30df0bcb",
            "secretKey": "a0ec3175c6c80e60bc8ef18bd7b73a631c507b9f0a42c973036c7f96d21b047a"}

client = CyberflyDataShipper(device_id="test", key_pair=key_pair)

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)


@client.on_message()
def do_something(data):
    pin_no = data.get("pin_no")
    status = data.get("status")
    GPIO.setup(pin_no, GPIO.OUT)
    if status=="on":
       GPIO.output(pin_no, GPIO.HIGH)
    else:
        GPIO.output(pin_no, GPIO.LOW)

while 1:
    client.update_data("temperature", 35)
    client.send_data()
    time.sleep(5) # time interval
```