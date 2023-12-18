from .configs import deviceConfig, displayConfig
from time import sleep_ms
from machine import Pin
from neopixel import NeoPixel
import uasyncio


class PixelHandler(object):
    _neopixel: NeoPixel
    _pin: Pin
    _async_task: uasyncio.Task | None = None

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

    def _set_display_pattern(self, pattern_colors: list[tuple]) -> None:
        pattern_length = len(pattern_colors)
        for pixel_address in range(deviceConfig.total_pixels):
            pixel_color = pattern_colors[pixel_address % pattern_length]
            self._neopixel[pixel_address] = pixel_color

        self._neopixel.write()

    async def _set_display_flash(self, color: tuple, speed: int) -> None:
        is_on = True
        while True:
            if is_on:
                self._neopixel.fill(color)
            else:
                self._neopixel.fill((0, 0, 0))
            self._neopixel.write()
            is_on = not is_on
            await uasyncio.sleep_ms(speed)

    async def _set_display_pattern_scroll(self, pattern_colors: list[tuple], speed: int) -> None:
        active_pattern = pattern_colors[:]

        while True:
            self._set_display_pattern(active_pattern)
            active_pattern.insert(0, active_pattern.pop())
            await uasyncio.sleep_ms(speed)

    async def set_display(self, display: dict):
        print('received: ', display)
        if self._async_task is None:
            print('no async_task')
        else:
            print('has task, cancele')
            self._async_task.cancel()
            self._async_task = None

        print('updating config')
        deviceConfig.display = display

        if display['type'] is None:
            print('no display type set')

        elif display['type'] == 'solid':
            self._set_display_solid(display['color'])

        elif display['type'] == 'flash':
            self._async_task = uasyncio.create_task(self._set_display_flash(display['color'], display['speed']))

        elif display['type'] == 'pattern':
            self._set_display_pattern(display['pattern'])

        elif display['type'] == 'scroll':
            self._async_task = uasyncio.create_task(
                self._set_display_pattern_scroll(display['pattern'], display['speed']))


pixel = PixelHandler()
