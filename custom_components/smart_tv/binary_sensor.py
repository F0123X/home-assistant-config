# # # # # # # # # # # # # # # # # # # # # # #
#                     #                     #
#                   #   #                   #
#                 #       #                 #
#               #           #               #
#             #     Home      #             #
#           #                   #           #
#         # # #   Assistant   # # #         #
#             #               #             #
#             #               #             #
#             #               #             #
#             #               #             #
#             # # # # # # # # #             #
#                                           #
# # # # # # # # # # # # # # # # # # # # # # #
# Empty File
from homeassistant.components.binary_sensor import (
    DEVICE_CLASSES_SCHEMA, PLATFORM_SCHEMA, BinarySensorDevice)

DOMAIN = 'smart_tv'

CONF_NAME = 'name'
DEFAULT_NAME = 'smart_tv_app'
CONF_HOST = 'host'
CONF_APP = 'app'
CONF_TIMEOUT = 'timeout'

def setup_platform(hass, config, add_entities, discovery_info=None):
    """ Set up sensor platform """
    add_devices(S)

class SmartTVAppSensor(Entity):

    def __init__(self, config):
        self._state = False
        self._name = config.get(CONF_NAME, 'Smart TV App')
    
    @property
    def name(self):
        return self._name

    @property
    def state(self):
        return self._state





def setup(hass, config):
    
    hass.states.set('smart_tv.is_on', 'yes')

    return True
