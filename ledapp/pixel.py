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
        return not (self._pin is None or self._neopixel is None)

    async def _apply_state_from_config(self):
        last_state = displayConfig.state
        if last_state is None:
            self.set_state(True)
        else:
            self.set_state(last_state, False)

    async def _apply_value_from_config(self) -> None:
        last_display = displayConfig.value
        if last_display is not None:
            await self.set_display(last_display, False)

    async def apply_from_config(self) -> None:
        await self._apply_state_from_config()
        await self._apply_value_from_config()

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

    async def set_state(self, state: bool, store_update: bool = True) -> None:
        if store_update:
            displayConfig.state = state

        if state:
            # set value to prior value
            await self._apply_value_from_config()
        else:
            self._set_display_solid((0, 0, 0))

    def process_value(self, value: dict) -> dict:
        if 'color' in value and value['color'] is not None:
            value['color'] = tuple(value['color'])

        if 'pattern' in value and value['pattern'] is not None:
            value['pattern'] = map(tuple, value['pattern'])

        return value

    async def set_display(self, display: dict, store_update: bool = True) -> None:
        if store_update:
            displayConfig.value = display

        display = self.process_value(display)

        print('received: ', display)
        if self._async_task is None:
            print('no async_task')
        else:
            print('has task, cancele')
            self._async_task.cancel()
            self._async_task = None

        if not displayConfig.state:
            self._set_display_solid((0, 0, 0,))
            return None

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
