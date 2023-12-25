from .mqtt_as import MQTTClient, config
from .pixel import pixelHandler
from .configs import mqttConfig
import network
import ubinascii
import uasyncio
import json

loop = uasyncio.get_event_loop()

network_mac_address = ubinascii.hexlify(network.WLAN(network.STA_IF).config('mac')).decode()

if mqttConfig.in_group is None:
    mqttConfig.in_group = True
    mqttConfig.group = 'main_decoration'

device_topic_prefix = 'devices/{}'.format(network_mac_address)

control_topic_type = 'groups' if mqttConfig.in_group else 'devices'
control_topic_identifier = mqttConfig.group if mqttConfig.in_group else network_mac_address

control_topic_prefix = '{}/{}'.format(control_topic_type, control_topic_identifier)

mqtt_topics = {
    'connection': '{}/online'.format(device_topic_prefix),
    'config': '{}/config'.format(device_topic_prefix),
    "status": '{}/status'.format(control_topic_prefix),
    "display": '{}/display'.format(control_topic_prefix),
}


async def messages(client):  # Respond to incoming messages
    print('starting messages')
    async for topic, msg, retained in client.queue:
        try:
            topic_string = topic.decode('utf-8')
            message_json = json.loads(msg.decode('utf-8'))

            if topic_string == mqtt_topics['display']:
                # await pixelHandler.set_display(self.data)
                await pixelHandler.set_display(message_json)
            elif topic_string == mqtt_topics['status']:
                await pixelHandler.set_status(message_json)
            elif topic_string == mqtt_topics['config']:
                print('set config: ', message_json)
        except Exception as e:
            print("error in handling message: ", e)


async def up(client):  # Respond to connectivity being (re)established
    while True:
        print('starting up')
        await client.up.wait()  # Wait on an Event
        client.up.clear()
        # subscribe to status changes
        await client.subscribe(mqtt_topics['status'], 1)
        # subscribe to display changes
        await client.subscribe(mqtt_topics['display'], 0)
        # subscribe to config changes
        await client.subscribe(mqtt_topics['config'], 1)
        # publish device connected
        client.publish(mqtt_topics['connection'], json.dumps(True), True, 1)


async def wifi_handler(is_connected: bool) -> None:
    if not is_connected:
        # not connected so run last config
        await pixelHandler.run()


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

# wifi connection handler
config['wifi_coro'] = wifi_handler

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
