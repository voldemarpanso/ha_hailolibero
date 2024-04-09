"""Platform for Hailolibero sensor integration."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable

from homeassistant.components.sensor import (SensorEntity, SensorEntityDescription)
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.helpers.entity import EntityCategory, DeviceInfo

from .const import DOMAIN, HAILO_DEVICES
from . import HailoDevice

import logging

_LOGGER = logging.getLogger(__name__)

class HailoRequiredKeysMixin:
    """Mixin for required keys."""
    value_fn: Callable[[Any], float]
    enabled: Callable[[Any], bool]

@dataclass
class HailoSensorEntityDescription(
    SensorEntityDescription, HailoRequiredKeysMixin
):
    """Describes Hailo sensor entities."""

HAILO_SENSORS: tuple[HailoSensorEntityDescription, ...] = (

    HailoSensorEntityDescription(
        key="status",
        name="Status",
        icon="mdi:thumb-up",
        entity_category=EntityCategory.DIAGNOSTIC,
        value_fn=lambda device: device.info.status,
        enabled=lambda device: True,
        entity_registry_enabled_default=True,
    ),
    HailoSensorEntityDescription(
        key="ipconf",
        name="IP Settings",
        icon="mdi:network",
        entity_category=EntityCategory.DIAGNOSTIC,
        value_fn=lambda device: "Autmatic (DHCP)" if device.settings.ipconf else "Static",
        enabled=lambda device: True,
        entity_registry_enabled_default=True,
    ),
    HailoSensorEntityDescription(
        key="ssid",
        name="SSID",
        icon="mdi:wifi-cog",
        entity_category=EntityCategory.DIAGNOSTIC,
        value_fn=lambda device: device.settings.ssid,
        enabled=lambda device: True,
        entity_registry_enabled_default=True,
    ),
)

async def async_setup_entry(hass, entry, async_add_entities: AddEntitiesCallback):
    """Add sensors for passed config_entry in HA."""
    entry_config = hass.data[DOMAIN][entry.entry_id]

    hailo_devices = entry_config.get(HAILO_DEVICES)

    entities = []
    entities.extend([
        HailoSensorDevice(hailo_device, description)
        for description in HAILO_SENSORS
        for hailo_device in hailo_devices
        if description.enabled(hailo_device)
    ])
    async_add_entities(entities)

class HailoSensorDevice(CoordinatorEntity, SensorEntity):
    """Representation of a sensor."""
    entity_description: HailoSensorEntityDescription
    
    def __init__(
            self,
            device: HailoDevice,
            description: HailoSensorEntityDescription,
    ) -> None:
        """Initialize the sensor."""

        super().__init__(device._coordinator)
        self._device: HailoDevice = device
        self._attr_name = f"{description.name}"
        self._attr_unique_id = f"{device.info.device}-{description.key}"
        self.entity_description = description
        
    @property
    def native_value(self):
        """Return the state of the sensor."""
        return self.entity_description.value_fn(self._device)

    @property
    def device_info(self) -> DeviceInfo:
        """Return a device description for device registry."""
        return self._device.device_info   
    