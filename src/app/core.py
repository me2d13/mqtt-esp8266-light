#import sys
#sys.path.append('/app')

# ampy -p COM6 put main.py main.py

import app.wifi
import machine
from app.ota_updater import OTAUpdater
import app.secrets as secrets
from app.state import State
from app.mqtt import init_mqtt
from app.light import Light
import utime

def check_for_updates():
    print('Checking for updates...')
    otaUpdater = OTAUpdater(secrets.GITHUB_URL, github_src_dir='src', main_dir='app', secrets_file="secrets.py")
    was_installed = False
    version = '?'
    try:
        (was_installed, version) = otaUpdater.install_update_if_available()
    except Exception as e:
        print('Error during update check:', e)
    del(otaUpdater)
    if was_installed:
        print('Update to version {} installed, reboot...'.format(version))
        machine.reset()
        utime.sleep(5)
    else:
        print('Current version {} ok, no new version found'.format(version))
    return version

def init_state():
    state = State()
    try:
        state.load_state()
    except OSError as e:
        print("State not loaded, probbly file doesn't exist", e)
    return state


def main():
    app.wifi.connect_wifi()
    version = check_for_updates()
    state = init_state()
    light = Light(state)
    client = init_mqtt(state, light, version)
    while True:
        client.wait_msg()
    client.disconnect()
    state.save_state()
