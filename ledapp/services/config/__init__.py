from .config_handler import ConfigHandler

networkConfig = ConfigHandler("/config/network.json")
deviceConfig = ConfigHandler("/config/device.json")
mqttConfig = ConfigHandler("/config/mqtt.json")
