from .configs import deviceConfig, displayConfig
from time import sleep_ms
from machine import Pin
from neopixel import NeoPixel
import _thread
import uasyncio


class PixelHandler:
    _neopixel: NeoPixel
    _pin: Pin
    # _async_task: uasyncio.

    def __init__(self):
        self.config = deviceConfig
        config_pin = deviceConfig.pin
        config_total_pixels = deviceConfig.total_pixels
        self._pin = Pin(config_pin, mode=Pin.OUT)
        self._neopixel = NeoPixel(self._pin, config_total_pixels)

    @property
    def is_setup(self) -> bool:
        return self._pin is not None or self._neopixel is not None

    def _set_display_solid(self, color: tuple) -> None:
        self._neopixel.fill(color)
        self._neopixel.write()

    async def _set_display_flash(self, color: tuple, speed: int) -> None:
        is_on = True
        while (self.config.display['speed'] is not None
               and self.config.display['type'] == 'flash'
               and self.config.display['color'] != color):
            if is_on:
                self._neopixel.fill(color)
            else:
                self._neopixel.fill((0, 0, 0))
            self._neopixel.write()
            is_on = not is_on
            await uasyncio.sleep_ms(speed)

    async def set_display(self, display: dict):
        if self._async_task is not None:
            self._async_task.cancel()

        deviceConfig.display = display

        if display['type'] is None:
            print('no display type set')

        elif display['type'] == 'solid':
            self._set_display_solid(display['color'])

        elif display['type'] == 'flash':
            self._async_task = uasyncio.create_task(self._set_display_flash(display['color'], display['speed']))



pixel = PixelHandler()
