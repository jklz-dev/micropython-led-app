import uasyncio
import json
from umqtt.simple import MQTTClient
from .pixel import pixelHandler
from .async_provider import asyncProvider
from ledapp.configs import mqttConfig

_topic_display = 'groups/kitchen_top/display'
_topic_status = 'groups/kitchen_top/status'
_topic_online = 'devices/{}/online'.format(mqttConfig.device)


class MqttReceiver:
    topic: str | None = None
    message: str | None = None
    data: dict | bool | None = None

    def reset(self):
        print("reset")
        self.topic = None
        self.message = None
        self.data = None

    def __call__(self, topic, message):
        print("__call__")
        self.topic = topic.decode('utf-8')
        self.message = message.decode('utf-8')

    @property
    def has_data(self):
        return self.topic is not None and self.message is not None

    async def consume(self):
        print("Consuming message")
        try:
            self.data = json.loads(self.message)

            if self.topic == _topic_display:
                # await pixelHandler.set_display(self.data)
                await pixelHandler.set_display(self.data)
            elif self.topic == _topic_status:
                await pixelHandler.set_status(self.data)
        except Exception as e:
            print("error in handling message: ", e)

        self.reset()


receiver = MqttReceiver()


async def handle_callback(topic, message):
    print("Consuming message")
    try:
        data = json.loads(message)

        if topic == _topic_display:
            # await pixelHandler.set_display(self.data)
            await pixelHandler.set_display(data)
        elif topic == _topic_status:
            await pixelHandler.set_status(data)
    except Exception as e:
        print("error in handling message: ", e)


def sub_callback(topic, message):
    asyncProvider.subscribe(handle_callback(topic, message))


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
    client.set_last_will(_topic_online, json.dumps(False), True, 1)
    client.connect()
    client.set_callback(receiver)

    client.publish(_topic_online, json.dumps(True), True, 1)

    client.subscribe(_topic_status, 1)
    client.subscribe(_topic_display, 0)

    return client


async def mqtt_handler():
    # setup connection
    client = create_mqtt_client()
    # consume messages
    while True:
        print('checking for message')
        await client.check_msg()
        uasyncio.sleep(1)


def receive_messages():
    asyncProvider.run_main(mqtt_handler())
