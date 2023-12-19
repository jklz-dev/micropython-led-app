from .display_demo import run_demo
from .pixel import pixel
from .mqtt import create_mqtt_client, async_receive_messages, MQTTClient
import uasyncio


async def run(is_online: bool = False) -> None:
    # run app from package
    raise Exception("Not implemented")



async def run_app_async(is_online: bool = False, mqtt_client: MQTTClient | None = None) -> None:
    print('running ledapp async')
    # attempt to display from config
    await pixel.apply_from_config()
    if is_online and mqtt_client is not None:
        await async_receive_messages(mqtt_client)


def run_app(is_online: bool = False) -> None:
    # run app from package
    print('running ledapp')
    if not is_online:
        uasyncio.run(run_app_async(is_online))
    else:
        client = create_mqtt_client()
        uasyncio.run(run_app_async(is_online, client))


