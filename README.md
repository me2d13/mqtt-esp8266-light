# mqtt-esp8266-light
Just another MQTT controlled RGB light for Home Assistant on ESP8266 (Wemos D1) - this time using micropython

# Notes and links
* inspired by https://github.com/Giannie/Micropython-HASS-Neopixel-MQTT-Light
* using OTA with https://github.com/rdehuyss/micropython-ota-updater
* Wemos D1 pin numbering as per https://www.mfitzp.com/article/wemos-d1-pins-micropython/ and other sites

## Upload via USB
```
cd src
ampy -p COM6 rmdir app
ampy -p COM6 put app app
```