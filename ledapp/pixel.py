from .configs import deviceConfig, displayConfig
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

        if displayConfig.state is None:
            displayConfig.state = True

    @property
    def is_setup(self) -> bool:
        return not (self._pin is None or self._neopixel is None)

    def _set_display_off(self):
        self._set_display_solid((0, 0, 0))

    def _set_display_solid(self, color: tuple) -> None:
        self._neopixel.fill(color)
        self._neopixel.write()

    def _set_display_pattern(self, pattern_colors: list[tuple]) -> None:
        try:
            pattern_length = len(pattern_colors)
            for pixel_address in range(deviceConfig.total_pixels):
                pixel_color = pattern_colors[pixel_address % pattern_length]
                self._neopixel[pixel_address] = pixel_color

            self._neopixel.write()
        except Exception as e:
            print('Exception: ', e)

    async def _set_display_flash(self, color: tuple, speed: int) -> None:
        is_on = True
        while True:
            print('update_flash: ', is_on)
            try:
                if is_on:
                    self._neopixel.fill(color)
                else:
                    self._neopixel.fill((0, 0, 0))
                self._neopixel.write()
            except Exception as e:
                print('Exception: ', e)
            is_on = not is_on
            await uasyncio.sleep_ms(speed)

    async def _set_display_pattern_scroll(self, pattern_colors: list[tuple], speed: int) -> None:
        active_pattern = pattern_colors[:]

        while True:
            print('update_pattern_scroll')
            try:
                self._set_display_pattern(active_pattern)
                active_pattern.insert(0, active_pattern.pop())
                print('update_pattern_scroll-pre-sleep')
                await uasyncio.sleep_ms(speed)
                print('update_pattern_scroll-post-sleep')
            except Exception as e:
                print("Can't update pattern scroll", e)

    async def set_status(self, state: bool) -> None:
        displayConfig.state = state

        print('set_status - pre-run')
        await self.run()
        print('set_status - post-run')

    def process_value(self, value: dict) -> dict:
        if 'color' in value and value['color'] is not None:
            value['color'] = tuple(value['color'])

        if 'pattern' in value and value['pattern'] is not None:
            value['pattern'] = list(map(tuple, value['pattern']))

        return value

    def set_display_value(self, display: dict):
        displayConfig.value = self.process_value(display)

    async def run(self) -> None:
        display = self.process_value(displayConfig.value)
        print('running value: ', display)
        # check if prior task running
        if self._async_task is None:
            print('no running async task')
        else:
            print('running task, will cancel')
            self._async_task.cancel()
            self._async_task = None

        if not displayConfig.state:
            self._set_display_off()
            return None

        if display['type'] is None:
            print('problem config')
            self._set_display_off()

        elif display['type'] == 'solid':
            self._set_display_solid(display['color'])

        elif display['type'] == 'flash':
            self._async_task = uasyncio.create_task(self._set_display_flash(display['color'], display['speed']))

        elif display['type'] == 'pattern':
            self._set_display_pattern(display['pattern'])

        elif display['type'] == 'scroll':
            self._async_task = uasyncio.create_task(
                self._set_display_pattern_scroll(display['pattern'], display['speed']))

        await uasyncio.sleep(0)

    async def set_display(self, display: dict) -> None:
        self.set_display_value(display)
        print('set_display - pre-run')
        await self.run()
        print('set_display - post-run')


pixelHandler = PixelHandler()
