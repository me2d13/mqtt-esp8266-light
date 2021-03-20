#import sys
#sys.path.append('/app')

# ampy -p COM6 put main.py main.py

import app.wifi
import machine
from app.ota_updater import OTAUpdater
from umqtt.robust import MQTTClient
import app.secrets as secrets
from app.state import State

def sub_cb(topic, msg):
    print((topic, msg))

def check_for_updates():
    print('Checking for updates...')
    otaUpdater = OTAUpdater(secrets.GITHUB_URL, github_src_dir='src', main_dir='app', secrets_file="secrets.py")
    was_installed = False
    try:
        was_installed = otaUpdater.install_update_if_available()
    except Exception as e:
        print('Error during update check:', e)
    del(otaUpdater)
    if was_installed:
        print('Update installed, reboot...')
        machine.reset()
    else:
        print('No new version found')

def init_state():
    state = State()
    try:
        state.load_state()
    except OSError as e:
        print("State not loaded, probbly fle doesn't exist", e)
    return state

def init_mqtt():
    client = MQTTClient("rgbled-pracovna", secrets.MQTT_HOST, secrets.MQTT_PORT)
    client.set_callback(sub_cb)
    client.connect()
    print('MQTT connected to', secrets.MQTT_HOST)
    client.subscribe(b"foo_topic")
    client.publish(secrets.BASE_TOPIC + "log", b"Device {} alive".format(secrets.BASE_TOPIC))
    return client

def main():
    state = init_state()
    client = init_mqtt()
    app.wifi.connect_wifi()
    check_for_updates()
    while True:
        client.wait_msg()
    client.disconnect()
    state.save_state()
