#import sys
#sys.path.append('/app')

import app.wifi
from app.ota_updater import OTAUpdater
from umqtt.robust import MQTTClient
import app.secrets as secrets

def sub_cb(topic, msg):
    print((topic, msg))

def main():
    app.wifi.connect_wifi()
    client = MQTTClient("rgbled-pracovna", secrets.MQTT_HOST, secrets.MQTT_PORT)
    client.set_callback(sub_cb)
    client.connect()
    print('MQTT connected to', secrets.MQTT_HOST)
    client.subscribe(b"foo_topic")
    client.publish(secrets.BASE_TOPIC + "log", b"Device {} alive".format(secrets.BASE_TOPIC))
    while True:
        client.wait_msg()
    client.disconnect()

main()