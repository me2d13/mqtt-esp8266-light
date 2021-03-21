# change real values and rename this file to secrets.py

WIFI_SSID = ''
WIFI_PASSWORD = ''
MQTT_HOST = '192.168.1.100'
MQTT_PORT = 1883
MQTT_CLIENT = 'rgbled'
STATE_TOPIC = '/devices/rgbled'
COMMAND_TOPIC = '/devices/rgbled/set'
LOG_TOPIC = '/devices/rgbled/log'
GITHUB_URL = 'https://github.com/me2d13/mqtt-esp8266-light'
PIN_R = 4 # Wemos D2
PIN_G = 0 # Wemos D3
PIN_B = 2 # Wemos D4
OUTPUT_INVERTED = True # By your HW design: When inverted 0 on PWM pin means full bright, 1023 means off