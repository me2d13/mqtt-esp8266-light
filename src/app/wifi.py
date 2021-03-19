import time, machine, network, gc
import app.secrets as secrets

print('Memory free', gc.mem_free())

def connect_wifi():
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('Connecting to network...')
        sta_if.active(True)
        sta_if.connect(secrets.WIFI_SSID, secrets.WIFI_PASSWORD)
        while not sta_if.isconnected():
            time.sleep_ms(100)
    print('network config:', sta_if.ifconfig())