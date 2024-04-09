"""Platform for Hailolibero number integration."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable

from homeassistant.components.number import (NumberDeviceClass, NumberEntity, 
                                             NumberEntityDescription)
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
class HailoNumberEntityDescription(
    NumberEntityDescription, HailoRequiredKeysMixin
):
    """Describes Hailo number entities."""

HAILO_NUMBERS: tuple[HailoNumberEntityDescription, ...] = (

    HailoNumberEntityDescription(
        key="led",
        name="Led Brightness",
        icon="mdi:lightbulb-on",
        entity_category=EntityCategory.CONFIG,
        value_fn=lambda device: device.settings.led,
        enabled=lambda device: True,
        entity_registry_enabled_default=True,
    ),
    HailoNumberEntityDescription(
        key="pwr",
        name="Pullout Force",
        icon="mdi:pickaxe",
        entity_category=EntityCategory.CONFIG,
        value_fn=lambda device: device.settings.pwr,
        enabled=lambda device: True,
        entity_registry_enabled_default=True,
    ),
    HailoNumberEntityDescription(
        key="dist",
        name="Detection Range",
        icon="mdi:ruler",
        entity_category=EntityCategory.CONFIG,
        device_class=NumberDeviceClass.DISTANCE,
        value_fn=lambda device: device.settings.dist,
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
        HailoNumberDevice(hailo_device, description)
        for description in HAILO_NUMBERS
        for hailo_device in hailo_devices
        if description.enabled(hailo_device)
    ])
    async_add_entities(entities)

class HailoNumberDevice(CoordinatorEntity, NumberEntity):
    """Representation of a Number."""
    entity_description: HailoNumberEntityDescription
    
    def __init__(
            self,
            device: HailoDevice,
            description: HailoNumberEntityDescription,
    ) -> None:
        """Initialize the number."""

        super().__init__(device._coordinator)
        self._device: HailoDevice = device
        self._attr_name = f"{description.name}"
        self._attr_unique_id = f"{device.info.device}-{description.key}"
        self.entity_description = description
        
    @property
    def native_value(self):
        """Return the state of the number."""
        return self.entity_description.value_fn(self._device).value

    @property
    def native_min_value(self):
        """Return min limit for the number."""
        return self.entity_description.value_fn(self._device).min

    @property
    def native_max_value(self):
        """Return max limit for the number."""
        return self.entity_description.value_fn(self._device).max

    @property
    def device_info(self) -> DeviceInfo:
        """Return a device description for device registry."""
        return self._device.device_info   
    
    async def async_set_native_value(self,  value: Any) -> None: 
        """ Set Hailo number device value"""
        _LOGGER.debug(f"async_set_native_value: {self.entity_description.key}: {value}")
        
        data = getattr(self._device.settings, self.entity_description.key)
        data.value = round(value);
        setattr(self._device.settings, self.entity_description.key, data)
        self._device.hailo.settings = self._device.settings

        result = await self._device.hailo.write_settings()
        return result
