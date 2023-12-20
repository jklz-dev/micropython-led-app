import json

from umqtt.simple import MQTTClient
import uasyncio
from .pixel import pixelHandler
from ledapp.configs import mqttConfig



_topic_display = 'groups/kitchen_top/display'
_topic_status = 'groups/kitchen_top/status'
_topic_online = 'devices/{}/online'.format(mqttConfig.device)

async def _subscribe(client: MQTTClient, topic, qos: int) -> None:
    client.subscribe(topic, qos)


def handle_callback(topic, message):
    topic_string = topic.decode('utf-8')
    message_string = message.decode('utf-8')

    try:
        message_data = json.loads(message_string)

        if topic_string == _topic_display:
            pixelHandler.set_display_value(message_data)
        elif topic_string == _topic_status:
            pixelHandler.set_status_value(message_data)
    except Exception as e:
        print("error in handling message: ", e)


def create_mqtt_client() -> MQTTClient:
    client = MQTTClient(
        mqttConfig.device,
        mqttConfig.host,
        port=0,
        user=bytes(mqttConfig.user, 'utf-8'),
        password=bytes(mqttConfig.password, 'utf-8'),
        keepalive=7200,
        ssl=True,
        ssl_params={'server_hostname': mqttConfig.host}
    )
    client.set_last_will(_topic_online, json.dumps(True), True, 1)
    client.connect()
    client.set_callback(handle_callback)

    client.publish(_topic_online, json.dumps(False), True, 1)

    _subscribe(client, _topic_status, 1)
    _subscribe(client, _topic_display, 0)

    return client


async def async_receive_messages(client: MQTTClient):
    print('async receive messages')
    while True:
        client.wait_msg()
        await pixelHandler.run()
        await uasyncio.sleep(1)
