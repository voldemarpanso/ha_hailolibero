# Hailo Libero 3.0 Integration (non-official)
![GitHub Release](https://img.shields.io/github/v/release/voldemarpanso/ha_hailolibero)
![GitHub Downloads (all assets, all releases)](https://img.shields.io/github/downloads/voldemarpanso/ha_hailolibero/total)
![GitHub Last Commit](https://img.shields.io/github/last-commit/voldemarpanso/ha_hailolibero)
![HA Badge](https://img.shields.io/badge/Home%20Assistant-%23FFFFFF?logo=homeassistant&link=https%3A%2F%2Fwww.home-assistant.io%2F)
![HACS Badge](https://img.shields.io/badge/Custom-%2341BDF5?label=HACS&link=https%3A%2F%2Fhacs.xyz%2Fdocs%2Ffaq%2Fcustom_repositories%2F)
![Static Badge](https://img.shields.io/badge/Buy%20me%20a%20beer-white?logo=paypal&label=Paypal&link=https%3A%2F%2Fwww.paypal.com%2Fdonate%2F%3Fbusiness%3DKRHMM8QBFCVJ2%26no_recurring%3D0%26item_name%3DBuy%2Bme%2Ba%2Bbeer%26currency_code%3DEUR)

## Disclaimer
This is not official integration from Hailo. It's made out of curiosity, fun and beer.

## Supported device
- https://www.hailo.de/en/built-in-technology/p/hailo-libero-30-3697301

## Installation
[![Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=voldemarpanso&repository=ha_hailolibero&category=integration)
- or add custom repo manually in HACS: https://github.com/voldemarpanso/ha_hailolibero


## Configuration
[![Open your Home Assistant instance and start setting up a new integration.](https://my.home-assistant.io/badges/config_flow_start.svg)](https://my.home-assistant.io/redirect/config_flow_start/?domain=hailo)
- or go to Settings -> Devices & Services
- Add Integration
- Search for Hailo
- Select and configure your Hailo

## Supported features
- Open
- Detection Range
- Led Brightness
- Pullout Force
- Restart

## Why? :)
To keep it closed when vacuum passes under it and reset to normal operation when vacuum is not cleaning.
Faster remote operation (via voice for example) - HA keeps it logged in, login seems to cause ~3sec delay, which makes it unusable, annoyingly slow, if you wish.
