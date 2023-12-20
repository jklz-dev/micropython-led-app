from .async_provider import asyncProvider
from .display_demo import run_demo
from .pixel import pixelHandler
from .configs import mqttConfig
from .mqtt import receive_messages


def run_app(is_online: bool = False, device_identifier: str | None = None) -> None:
    # run app from package
    print('running ledapp')
    if device_identifier is not None:
        mqttConfig.device = device_identifier

    elif mqttConfig.device is None:
        mqttConfig.device = "test-device"

    if is_online:
        receive_messages()

    else:
        asyncProvider.run_main(pixelHandler.run())
