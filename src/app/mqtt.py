from umqtt.robust import MQTTClient
import app.secrets as secrets

def sub_cb(topic, msg):
    print((topic, msg))


def init_mqtt(state):
    client = MQTTClient("rgbled-pracovna", secrets.MQTT_HOST, secrets.MQTT_PORT)
    client.set_callback(sub_cb)
    client.connect()
    print('MQTT connected to', secrets.MQTT_HOST)
    client.subscribe(b"foo_topic")
    if state.log_mqtt:
        client.publish(secrets.BASE_TOPIC + "log", b"Device {} alive".format(secrets.BASE_TOPIC))
    return client
