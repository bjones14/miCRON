'''

Defines the configuration class which is used to serialize/deserialize data
when loading/saving configurations.


'''

class config:

    def __init__(self, json_dict: dict):
        """
        Initializes and assigns config variables loaded from JSON file.

        Args:
            json_dict (dict): JSON dictionary that config is parsed from.
        """
        self._wifi_ssid = json_dict['_wifi_ssid']
        self._wifi_pass = json_dict['_wifi_pass']
        self._mqtt_server = json_dict['_mqtt_server']
        self._mqtt_user = json_dict['_mqtt_user']
        self._mqtt_pass = json_dict['_mqtt_pass']
        self._timezone_utc_offset = json_dict['_timezone_utc_offset']
        self._watchdog_timeout_ms = json_dict['_watchdog_timeout_ms']

    @property
    def wifi_ssid(self):
        return self._wifi_ssid

    @property
    def wifi_pass(self):
        return self._wifi_pass

    @property
    def mqtt_server(self):
        return self._mqtt_server

    @property
    def mqtt_user(self):
        return self._mqtt_user

    @property
    def mqtt_pass(self):
        return self._mqtt_pass

    def toJSON(self):
        return self.__dict__

