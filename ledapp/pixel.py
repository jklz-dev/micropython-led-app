from .configs import deviceConfig, displayConfig
from time import sleep_ms
from machine import Pin
from neopixel import NeoPixel
import uasyncio


class PixelHandler:
    _neopixel: NeoPixel
    _pin: Pin

    def __init__(self):
        config_pin = deviceConfig.pin
        config_total_pixels = deviceConfig.total_pixels
        self._pin = Pin(config_pin, mode=Pin.OUT)
        self._neopixel = NeoPixel(self._pin, config_total_pixels)

    @property
    def is_setup(self) -> bool:
        return self._pin is not None or self._neopixel is not None

    async def _set_display_solid(self, color: tuple) -> None:
        self._neopixel.fill(color)
        self._neopixel.write()

    async def _set_display_flash(self, color: tuple, speed: int) -> None:
        is_on = True
        while (deviceConfig.display['speed'] is not None
               and deviceConfig.display['type'] == 'flash'
               and deviceConfig.display['color'] != color):
            if is_on:
                self._neopixel.fill(color)
            else:
                self._neopixel.fill((0, 0, 0))
            self._neopixel.write()
            is_on = not is_on
            await uasyncio.sleep_ms(speed)
    async def async_set_display(self, display: dict) -> None:

        if display['type'] is None:
            print('no display type set')

        elif display['type'] == 'solid':
            uasyncio.create_task(self._set_display_solid(display['color']))

        elif display['type'] == 'flash':
            uasyncio.create_task(self._set_display_flash(display['color'], display['speed']))

    def set_display(self, display: dict):
        deviceConfig.display = display
        uasyncio.get_event_loop().run_until_complete(self.async_set_display(display))



pixel = PixelHandler()
