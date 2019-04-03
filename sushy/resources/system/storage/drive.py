#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

# This is referred from Redfish standard schema.
# http://redfish.dmtf.org/schemas/v1/Drive.v1_4_0.json

import logging

from sushy import exceptions
from sushy.resources import base
from sushy.resources import mappings as res_maps
from sushy import utils

LOG = logging.getLogger(__name__)


class Drive(base.ResourceBase):
    """This class represents a disk drive or other physical storage medium."""

    identity = base.Field('Id', required=True)
    """The Drive identity string"""

    indicator_led = base.MappedField('IndicatorLED',
                                     res_maps.INDICATOR_LED_VALUE_MAP)
    """Whether the indicator LED is lit or off"""

    name = base.Field('Name')
    """The name of the resource"""

    capacity_bytes = base.Field('CapacityBytes', adapter=utils.int_or_none)
    """The size in bytes of this Drive"""

    def set_indicator_led(self, state):
        """Set IndicatorLED to the given state.

        :param state: Desired LED state, lit (INDICATOR_LED_LIT), blinking
            (INDICATOR_LED_BLINKING), off (INDICATOR_LED_OFF)
        :raises: InvalidParameterValueError, if any information passed is
            invalid.
        """
        if state not in res_maps.INDICATOR_LED_VALUE_MAP_REV:
            raise exceptions.InvalidParameterValueError(
                parameter='state', value=state,
                valid_values=list(res_maps.INDICATOR_LED_VALUE_MAP_REV))

        data = {
            'IndicatorLED': res_maps.INDICATOR_LED_VALUE_MAP_REV[state]
        }

        self._conn.patch(self.path, data=data)
        self.invalidate()
