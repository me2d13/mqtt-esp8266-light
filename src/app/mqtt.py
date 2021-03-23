from umqtt.robust import MQTTClient
import app.secrets as secrets
import ujson

def dispatch_message(topic, msg, light):
    topic = topic.decode("utf-8")
    msg = msg.decode("utf-8")
    print('Received MQTT message at {}'.format(topic), msg)
    try:
        parsed = ujson.loads(msg)
        light.on_message(parsed)
    except ValueError as e:
        print('Json parsing error', e)
        light.log_function('Json parsing error for ' + msg)


def init_mqtt(state, light, version):
    def callback_with_light(topic, msg):
        dispatch_message(topic, msg, light)

    def mqtt_log(message):
        client.publish(secrets.LOG_TOPIC, message)

    client = MQTTClient(secrets.MQTT_CLIENT, secrets.MQTT_HOST, secrets.MQTT_PORT)
    client.set_callback(callback_with_light)
    client.connect()
    print('MQTT connected to', secrets.MQTT_HOST)
    client.subscribe(secrets.COMMAND_TOPIC)
    print('MQTT subscribed to', secrets.COMMAND_TOPIC)
    if state.log_mqtt:
        client.publish(secrets.LOG_TOPIC, "Device {} alive with version {}".format(secrets.STATE_TOPIC, version))
        light.log_function = mqtt_log

    return client
