import json

from umqtt.simple import MQTTClient
import uasyncio
from .pixel import pixel
from ledapp.configs import mqttConfig


_topic_display = 'groups/kitchen_top/display'
_topic_status = 'groups/kitchen_top/status'

async def _subscribe(client: MQTTClient, topic, qos: int) -> None:
    client.subscribe(topic, qos)


async def async_handle_callback(topic, message):
    topic_string = topic.decode('utf-8')
    message_string = message.decode('utf-8')

    try:
        message_data = json.loads(message_string)

        if topic_string == _topic_display:
            await pixel.set_display(message_data)
        elif topic_string == _topic_status:
            await pixel.set_status(message_data)
    except Exception as e:
        print("error in handling message: ", e)


def create_mqtt_client() -> MQTTClient:
    client = MQTTClient(
        'client_test_id',
        mqttConfig.host,
        port=0,
        user=bytes(mqttConfig.user, 'utf-8'),
        password=bytes(mqttConfig.password, 'utf-8'),
        keepalive=7200,
        ssl=True,
        ssl_params={'server_hostname': mqttConfig.host}
    )
    client.connect()
    client.set_callback(lambda topic, msg: uasyncio.create_task(async_handle_callback(topic, msg)))

    uasyncio.create_task(_subscribe(client, _topic_status, 1))
    uasyncio.create_task(_subscribe(client, _topic_display, 0))

    return client


async def async_receive_messages(client: MQTTClient):
    print('async receive messages')
    while True:
        message_response = client.wait_msg()
        if message_response is not None:
            print(message_response)
            # uasyncio.create_task(async_handle_callback(message_response))
        await uasyncio.sleep(1)
