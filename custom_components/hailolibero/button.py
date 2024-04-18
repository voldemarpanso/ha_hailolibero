"""Platform for Hailolibero Button integration."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable

from homeassistant.components.button import (ButtonEntity, ButtonDeviceClass,
                                             ButtonEntityDescription)
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.helpers.entity import DeviceInfo, EntityCategory

from .const import DOMAIN, HAILO_DEVICES
from . import HailoDevice

import logging

_LOGGER = logging.getLogger(__name__)

class HailoRequiredKeysMixin:
    """Mixin for required keys."""
    press_fn: Callable[[Any], float]
    enabled: Callable[[Any], bool]

@dataclass
class HailoButtonEntityDescription(
    ButtonEntityDescription, HailoRequiredKeysMixin
):
    """Describes Hailo button entities."""

HAILO_BUTTONS: tuple[HailoButtonEntityDescription, ...] = (

    HailoButtonEntityDescription(
        key="push",
        name="Open Hailo",
        icon="mdi:hand-back-right",
        enabled=lambda device: True,
        press_fn=lambda device: device.hailo.open(),
        entity_registry_enabled_default=True,
    ),
    HailoButtonEntityDescription(
        key="restart",
        name="Restart",
        #icon="mdi:hand",
        device_class=ButtonDeviceClass.RESTART,
        entity_category=EntityCategory.DIAGNOSTIC,
        enabled=lambda device: True,
        press_fn=lambda device: device.hailo.restart(),
        entity_registry_enabled_default=True,
    ),
)

async def async_setup_entry(hass, entry, async_add_entities: AddEntitiesCallback):
    """Add sensors for passed config_entry in HA."""
    entry_config = hass.data[DOMAIN][entry.entry_id]

    hailo_devices = entry_config.get(HAILO_DEVICES)

    entities = []
    entities.extend([
        HailoButtonDevice(hailo_device, description)
        for description in HAILO_BUTTONS
        for hailo_device in hailo_devices
        if description.enabled(hailo_device)
    ])

    async_add_entities(entities)

class HailoButtonDevice(CoordinatorEntity, ButtonEntity):
    """Representation of a Button."""
    entity_description: HailoButtonEntityDescription
    
    def __init__(
            self,
            device: HailoDevice,
            description: HailoButtonEntityDescription,
    ) -> None:
        """Initialize the button."""

        super().__init__(device._coordinator)
        self._device: HailoDevice = device
        self._attr_name = f"{description.name}"
        self._attr_unique_id = f"{device.info.device}-{description.key}"
        self.entity_description = description

    @property
    def device_info(self) -> DeviceInfo:
        """Return a device description for device registry."""
        return self._device.device_info

    async def async_press(self):
        """ Push Hailo Libero."""
        _LOGGER.debug(f"async_press: {self.entity_description.key}")
        result = await self.entity_description.press_fn(self._device)
        return result

