import time
import ubinascii
import network


class WlanClient:
    _interface: network.WLAN

    error: str | None

    @staticmethod
    def is_supported() -> bool:
        return hasattr(network, "WLAN")

    def __init__(self):
        try:
            self._interface = network.WLAN(network.STA_IF)
            self._interface.active(True)
        except Exception as e:
            print('Error creating WLAN interface', e)

    @property
    def is_connected(self) -> bool:
        return self._interface.isconnected()

    @property
    def mac_address(self) -> str:
        interface_mac = self._interface.config('mac')
        return ubinascii.hexlify(interface_mac).decode()

    @property
    def interface_status(self):
        return self._interface.status()

    @property
    def ifconfig(self):
        return self._interface.ifconfig()

    @property
    def ip_address(self):
        if not self.is_connected:
            return None
        return self.ifconfig[0]

    def disconnect(self) -> None:
        if self.is_connected:
            self._interface.disconnect()

    def connect(self, ssid: str, password: str | None = None, max_wait: int = 10) -> None:
        if self.is_connected:
            self.disconnect()
        self._interface.active(False)
        self._interface.active(True)
        self.error = None

        self._interface.connect(ssid, password)
        print("WLAN connecting to [{}]".format(ssid))
        while max_wait > 0:
            if self.interface_status < 0 or self.interface_status >= 3:
                break

            max_wait -= 1
            print('WLAN connecting...')
            time.sleep(1)

        if self.interface_status != 3:
            # had error connecting
            self.error = 'network connection failed'
        else:
            print('WLAN connected')
            print("IP address: ", self.ip_address)


wirelessNetworkClient = WlanClient()
