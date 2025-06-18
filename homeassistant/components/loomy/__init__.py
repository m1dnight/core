from datetime import timedelta
import logging

from homeassistant.components.sensor import SensorEntity
from homeassistant.core import callback
from homeassistant.helpers.discovery import load_platform
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
    UpdateFailed,
)

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


async def async_setup(hass, config):
    # Data that you want to share with your platforms
    hass.data[DOMAIN] = {"watt": 23}

    load_platform(hass, "sensor", DOMAIN, {}, config)
    return True


async def async_setup_entry(hass, entry) -> bool:
    print("async setup entry")
    return True
