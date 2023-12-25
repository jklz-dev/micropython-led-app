from .mqtt_as import MQTTClient, config
from .pixel import pixelHandler
from .configs import mqttConfig
import network
import ubinascii
import uasyncio
import json

loop = uasyncio.get_event_loop()

network_mac_address = ubinascii.hexlify(network.WLAN(network.STA_IF).config('mac')).decode()

mqtt_topics = {
    'connection': 'devices/{}/online'.format(network_mac_address),
    "status": [
        'groups/kitchen_top/status',
        # 'groups/decoration/status',
    ],
    "display": [
        'groups/kitchen_top/display',
        # 'groups/decoration/display',
    ],
}


async def messages(client):  # Respond to incoming messages
    print('starting messages')
    async for topic, msg, retained in client.queue:
        try:
            topic_string = topic.decode('utf-8')
            message_json = json.loads(msg.decode('utf-8'))

            if topic_string in mqtt_topics['display']:
                # await pixelHandler.set_display(self.data)
                await pixelHandler.set_display(message_json)
            elif topic_string in mqtt_topics['status']:
                await pixelHandler.set_status(message_json)
        except Exception as e:
            print("error in handling message: ", e)


async def up(client):  # Respond to connectivity being (re)established
    while True:
        print('starting up')
        await client.up.wait()  # Wait on an Event
        client.up.clear()
        for topic in mqtt_topics['status']:
            await client.subscribe(topic, 1)

        for topic in mqtt_topics['display']:
            await client.subscribe(topic, 0)

        client.publish(mqtt_topics['connection'], json.dumps(True), True, 1)


async def app_main(client):
    global loop
    await client.connect()
    for coroutine in (up, messages):
        uasyncio.create_task(coroutine(client))
    while True:
        await uasyncio.sleep(1)


config['user'] = mqttConfig.user
config['password'] = mqttConfig.password
broker = mqttConfig.host  # e.g long_hex_string.s2.eu.hivemq.cloud
config['server'] = broker
config['ssl'] = True
config['ssl_params'] = {"server_hostname": broker}
# on disconnect
config['will'] = (mqtt_topics['connection'], json.dumps(False), True, 1)

config["queue_len"] = 1
MQTTClient.DEBUG = False  # Optional: print diagnostic messages


def app_run(wifi_ssid: str, wifi_password: str):
    global config
    config['ssid'] = wifi_ssid
    config['wifi_pw'] = wifi_password
    client = MQTTClient(config)
    try:
        uasyncio.run(app_main(client))
    finally:
        client.close()  # Prevent LmacRxBlk:1 errors
