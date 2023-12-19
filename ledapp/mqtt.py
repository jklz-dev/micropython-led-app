from umqtt.simple import MQTTClient
import uasyncio
from ledapp.configs import mqttConfig


async def _subscribe(client: MQTTClient, topic, qos: int) -> None:
    client.subscribe(topic, qos)


async def async_handle_callback(topic, message):
    print('async: ', topic, message)
    pass


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

    uasyncio.create_task(_subscribe(client, 'groups/kitchen_top/status', 1))
    uasyncio.create_task(_subscribe(client, 'groups/kitchen_top/display', 0))

    return client


async def async_receive_messages(client: MQTTClient):
    print('async receive messages')
    while True:
        message_response = client.wait_msg()
        if message_response is not None:
            print(message_response)
            # uasyncio.create_task(async_handle_callback(message_response))
        await uasyncio.sleep(1)
