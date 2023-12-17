from .configs import deviceConfig, displayConfig
from time import sleep_ms
from machine import Pin
from neopixel import NeoPixel

class PixelHandler:
    _neopixel: NeoPixel
    _pin: Pin

    @property
    def is_setup(self) -> bool:
        return self._pin is not None and self._neopixel is not None

    def _ensure_configured(self):
        if self.is_setup:
           return None

        self._pin = Pin(deviceConfig.pin, mode=Pin.OUT)
        self._neopixel = NeoPixel(self._pin, deviceConfig.total_pixels)

    def _set_display_solid(self, color: tuple) -> None:
        self._neopixel.fill(color)
        self._neopixel.write()

    def _set_display_flash(self, color: tuple, speed: int) -> None:
        is_on = True
        while deviceConfig.display['speed'] is not None and deviceConfig.display['type'] == 'flash':
            if is_on:
                self._neopixel.fill(color)
            else:
                self._neopixel.fill(0, 0, 0)
            self._neopixel.write()
            is_on = not is_on
            sleep_ms(speed)

    def set_display(self, display: dict):
        deviceConfig.display = display

        if display['type'] is None:
            print('no display type set')

        elif display['type'] == 'solid':
            self._set_display_solid(display['color'])

        elif display['type'] == 'flash':
            self._set_display_flash(display['color'], display['speed'])


pixel = PixelHandler()
