import uasyncio
import json
from umqtt.simple import MQTTClient
from .pixel import pixelHandler
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

    async def consume(self):
        print("Consuming message")
        try:
            self.data = json.loads(self.message)

            if self.topic == _topic_display:
                await pixelHandler.set_display(self.data)
            elif self.topic == _topic_status:
                await pixelHandler.set_status(self.data)
        except Exception as e:
            print("error in handling message: ", e)

        self.reset()


receiver = MqttReceiver()


def handle_callback(topic, message):
    topic_string = topic.decode('utf-8')
    message_string = message.decode('utf-8')

    try:
        message_data = json.loads(message_string)

        if topic_string == _topic_display:
            pixelHandler.set_display(message_data)
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
    client.set_last_will(_topic_online, json.dumps(False), True, 1)
    client.connect()
    client.set_callback(receiver)

    client.publish(_topic_online, json.dumps(True), True, 1)

    client.subscribe(_topic_status, 1)
    client.subscribe(_topic_display, 0)

    return client


async def receive_messages(client: MQTTClient):
    while True:
        try:
            print('waiting for messages')
            client.wait_msg()
            print('consume message')
            await receiver.consume()

        except Exception as e:
            print("error in receiving messages: ", e)

        uasyncio.sleep(3)
