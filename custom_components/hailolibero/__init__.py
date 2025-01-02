"""Hailo Libero integration."""

from __future__ import annotations

import logging

from typing import Iterable
from datetime import timedelta

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform, CONF_HOST, ATTR_MODEL, ATTR_SERIAL_NUMBER, ATTR_SW_VERSION
from homeassistant.core import HomeAssistant

from homeassistant.auth.providers.homeassistant import InvalidAuth
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
from homeassistant.helpers.importlib import async_import_module

from .const import DOMAIN, HAILO_DEVICES, MANUFACTURER, MODEL
from .config_flow import CannotConnect

_LOGGER = logging.getLogger(__name__)

SCAN_INTERVAL = timedelta(seconds=60)
MIN_TIME_BETWEEN_UPDATES = timedelta(seconds=60)

PLATFORMS: list[str] = [Platform.NUMBER, Platform.BUTTON, Platform.SENSOR]

async def async_setup_entity_platforms(
        hass: HomeAssistant,
        config_entry: ConfigEntry,
        platforms: Iterable[Platform | str],
) -> None:
        await hass.config_entries.async_forward_entry_setups(config_entry, platforms)

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Establish connection with Hailo."""

    module = await async_import_module(hass, "hailolibero")
    hailo = module.HailoLibero(
        ip_address=entry.data[CONF_HOST]
    )

    try:
        await async_auth(hailo)
    except (InvalidAuth, CannotConnect) as e:
        _LOGGER.error(f"Could not authenticate to {MANUFACTURER} {MODEL}: {e}")
        return False

    hailo_device = await hailo_device_setup(hass, hailo)

    hass.data.setdefault(DOMAIN, {}).setdefault(entry.entry_id, {}).update(
        {
            HAILO_DEVICES: [ hailo_device ],
        }
    )

    await async_setup_entity_platforms(hass, entry, PLATFORMS)
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    if unload_ok := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok

async def async_auth(hailo: HailoLibero):
    """Authenticate to Hailo Libero."""
    auth_result = await hailo.auth()
    if not auth_result:
        raise InvalidAuth

async def hailo_device_setup(hass: HomeAssistant, hailo: HailoLibero):
    """ Populate device data set it up """
    module = await async_import_module(hass, "hailolibero.hailolibero")
    await hailo.read_settings()
    hailo_device = HailoDevice(
        device={ "name": hailo.info.device },
        hailo=hailo,
        settings=module.HailoSettings,
        info=module.HailoInfo
    )
    await hailo_device.async_create_coordinator(hass)
    return hailo_device

class HailoDevice:
    def __init__(self, device, hailo: HailoLibero, settings, info):
        self.settings = settings
        self.info: info
        self.device = device
        self.latest_update = 0

        # self.device.add_update_callback(self.set_update_callback)
        """ Connection to Hailo """
        self.hailo: HailoLibero = hailo

        self._attr_available = 0
        self._available_threshold = 30
        self._coordinator: DataUpdateCoordinator | None = None
        self._extra_attributes = {}

        self.settings = hailo.settings
        self.info = hailo.info

    async def _async_update(self):
        """Pull the latest data from SaveConnect API."""
        _LOGGER.debug(f"_async_update attempt: %s", self.hailo.info.device)
       
        success = await self.hailo.read_settings()
        if success:
            self._attr_available = 0
        else:
            _LOGGER.warning("Update failed for %s", self.info.device)
            self._attr_available += 1
    
    async def async_create_coordinator(self, hass: HomeAssistant) -> None:
        """Get the coordinator for a specific device."""
        if self._coordinator:
            return

        coordinator = DataUpdateCoordinator(
            hass,
            _LOGGER,
            name=f"{DOMAIN}-{self.info.device}",
            update_method=self._async_update,
            # Polling interval. Will only be polled if there are subscribers.
            update_interval=SCAN_INTERVAL,
        )

        await coordinator.async_refresh()

        self._coordinator = coordinator

    @property
    def device_info(self) -> DeviceInfo:
        """Return a device description for device registry."""
        _device_info = DeviceInfo(
            identifiers={(DOMAIN, self.info.device)},
            manufacturer = MANUFACTURER,
            name = MANUFACTURER + " " + MODEL,
            model = MODEL
        )
        _device_info[ATTR_MODEL] = f"{MANUFACTURER} {MODEL} ({self.info.device})"
        _device_info[ATTR_SW_VERSION] = self.info.firmware

        return _device_info
