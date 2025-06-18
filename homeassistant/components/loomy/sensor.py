"""Platform for sensor integration."""

from __future__ import annotations

import logging
import random

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
from homeassistant.const import UnitOfTemperature
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
)

_LOGGER = logging.getLogger(__name__)
from datetime import timedelta


def setup_platform(
    hass: HomeAssistant,
    config: ConfigType,
    add_entities: AddEntitiesCallback,
    discovery_info: DiscoveryInfoType | None = None,
) -> None:
    print("setup platform")

    coordinator = MyCoordinator(hass)
    sensor = MyEntity(coordinator, 0)
    # add_entities([ExampleSensor(), sensor])
    add_entities([sensor])


class ExampleSensor(SensorEntity):
    """Representation of a Sensor."""

    _attr_name = "injection"
    _attr_native_unit_of_measurement = UnitOfTemperature.CELSIUS
    _attr_device_class = SensorDeviceClass.TEMPERATURE
    _attr_state_class = SensorStateClass.MEASUREMENT

    def update(self) -> None:
        """Fetch new state data for the sensor.

        This is the only method that should fetch new data for Home Assistant.
        """
        print("update sensor")
        self._attr_native_value = 23


class MyCoordinator(DataUpdateCoordinator):
    """My custom coordinator."""

    def __init__(self, hass):
        """Initialize my coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            # Name of the data. For logging purposes.
            name="My sensor",
            # Polling interval. Will only be polled if there are subscribers.
            update_interval=timedelta(seconds=1),
            # Set always_update to `False` if the data returned from the
            # api can be compared via `__eq__` to avoid duplicate updates
            # being dispatched to listeners
            always_update=True,
        )
        print("init")

    async def _async_setup(self):
        print("async setup")

    async def _async_update_data(self):
        print("async update")
        return {"value": random.randint(3, 9)}


class MyEntity(CoordinatorEntity, SensorEntity):
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_has_entity_name = True

    def __init__(self, coordinator, idx):
        """Pass coordinator to CoordinatorEntity."""
        super().__init__(coordinator)
        self.idx = idx
        self._device_name = "uwmaisuwpa"
        self._attr_name = "uwmaisuwpa"
        self._attr_native_value = 1245
        self._attr_unique_id = "uniqueasfuck"
        self._received_data_at_least_once = False
        self._available = True
        self._attr_device_info = DeviceInfo(
            configuration_url="https://www.kraken.com/",
            entry_type="service",
            identifiers={("loomy", "_".join(self._device_name.split(" ")))},
            manufacturer="loomy.be",
            name=self._device_name,
        )

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        # self._attr_is_on = self.coordinator.data[self.idx]["state"]
        # self.async_write_ha_state()
        print("handle coordinator update")
        print(self.coordinator.data["value"])
        self._attr_native_value = self.coordinator.data["value"]
        super()._handle_coordinator_update()

    async def async_turn_on(self, **kwargs):
        print("async turn on")
