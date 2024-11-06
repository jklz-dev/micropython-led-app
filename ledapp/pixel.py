from .configs import deviceConfig, displayConfig
from machine import Pin
from neopixel import NeoPixel
import uasyncio
from .matrix import Matrix
from .weather import Weather


class PixelHandler(object):
    _neopixel: NeoPixel
    _pin: Pin
    _async_task: uasyncio.Task | None = None

    def __init__(self):
        self.config = deviceConfig
        config_pin = deviceConfig.pin
        config_total_pixels = deviceConfig.total_pixels
        self._pin = Pin(config_pin, mode=Pin.OUT)
        self._neopixel = NeoPixel(pin=self._pin, n=config_total_pixels)
        # set to use colors as rgb
        self._neopixel.ORDER = (0, 1, 2, 3)

        if displayConfig.state is None:
            displayConfig.state = True
        # TODO: use device config for matrix config
        Matrix.configure(13, 13)

    @property
    def is_setup(self) -> bool:
        return not (self._pin is None or self._neopixel is None)

    def wheel(self, pos: int) -> tuple[int, int, int]:
        # Input a value 0 to 255 to get a color value.
        # The colours are a transition r - g - b - back to r.
        if pos < 0 or pos > 255:
            return (0, 0, 0)
        if pos < 85:
            return (255 - pos * 3, pos * 3, 0)
        if pos < 170:
            pos -= 85
            return (0, 255 - pos * 3, pos * 3)
        pos -= 170
        return (pos * 3, 0, 255 - pos * 3)

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

    def _set_display_single_pattern(self, pattern_colors: list[tuple], fill_color: tuple = None) -> None:
        try:
            if fill_color is not None:
                self._neopixel.fill(fill_color)
            pattern_length = len(pattern_colors)
            for pixel_address in range(pattern_length):
                try:
                    pixel_color = pattern_colors[pixel_address] or None
                except IndexError:
                    # catch if ever doesn't exist (shouldn't happen)
                    pixel_color = None
                if pixel_color is not None:
                    # set pixel color
                    self._neopixel[pixel_address] = pixel_color
            self._neopixel.write()
        except Exception as e:
            print('Exception: ', e)

    def _set_display_single_pattern_on_base(self, pattern_colors: list[tuple], base_pattern_colors: list[tuple]) -> None:
        try:
            for pixel_address in range(deviceConfig.total_pixels):
                try:
                    base_pixel_color = base_pattern_colors[pixel_address] or None
                except IndexError:
                    base_pixel_color = None

                try:
                    pixel_color = pattern_colors[pixel_address] or base_pixel_color
                except IndexError:
                    pixel_color = base_pixel_color

                if pixel_color is not None:
                    # set pixel color
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

    async def _set_display_rainbow(self, speed: int) -> None:
        num_pixels = deviceConfig.total_pixels
        while True:
            for j in range(255):
                self._neopixel.fill(self.wheel(j & 255))
                self._neopixel.write()
                await uasyncio.sleep_ms(speed)

    async def _set_display_rainbow_scroll(self, speed: int) -> None:
        num_pixels = deviceConfig.total_pixels
        while True:
            for j in range(255):
                for pixel_address in range(deviceConfig.total_pixels):
                    rc_index = (pixel_address * 256 // num_pixels) + j
                    self._neopixel[pixel_address] = self.wheel(rc_index & 255)
                self._neopixel.write()
                await uasyncio.sleep_ms(speed)

    async def _set_display_playback(self, frames: list[dict], base: list[tuple] = None) -> None:
        active_frames = frames[:]
        # if base is not None:
        #     # set base to be displayed
        #     print("has base config")

        while True:
            await uasyncio.sleep_ms(500)
            print('update_playback')
            try:
                # get next frame to display
                next_frame = active_frames.pop(0)
                # print("next frame: {}".format(next_frame))
                #  add next frame to end of list
                active_frames.append(next_frame)
                # play next frame
                if next_frame['type'] == 'pattern':
                    await self._set_display_playback_frame_pattern(next_frame['pattern'], next_frame['delay'])
                else:
                    print("unknown frame type: {}".format(next_frame['type']))
                # await uasyncio.sleep_ms(2000)
                # print("frame delay: {}".format(next_frame['delay']))
                # await uasyncio.sleep_ms(next_frame['delay'])
            except Exception as e:
                print("Can't update playback frame", e)

    async def _set_display_playback_frame_pattern(self, pattern_colors: list[tuple], delay_time: int) -> None:
        # display pattern
        self._set_display_single_pattern(pattern_colors, (0, 0, 0))
        print('playback_frame_pattern-pre-sleep')
        await uasyncio.sleep_ms(delay_time)
        print('playback_frame_pattern-post-sleep')
        return None

    async def _set_display_weather(self, display: dict):
        playback = Weather().with_weather(display).to_display_playback()
        print("weather")
        print(playback)
        await self._set_display_playback(playback['frames'])

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

        elif display['type'] == 'rainbow':
            self._async_task = uasyncio.create_task(self._set_display_rainbow(display['speed']))

        elif display['type'] == 'playback':
            self._async_task = uasyncio.create_task(self._set_display_playback(display['frames']))

        elif display['type'] == 'weather':
            self._async_task = uasyncio.create_task(self._set_display_weather(display))

        await uasyncio.sleep(0)

    async def set_display(self, display: dict) -> None:
        self.set_display_value(display)
        print('set_display - pre-run')
        await self.run()
        print('set_display - post-run')


pixelHandler = PixelHandler()
