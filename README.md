# Hailo Libero 3.0 Integration (non-official)
[![GitHub Release](https://img.shields.io/github/v/release/voldemarpanso/ha_hailolibero)](https://github.com/voldemarpanso/ha_hailolibero/)
[![GitHub Downloads (all assets, all releases)](https://img.shields.io/github/downloads/voldemarpanso/ha_hailolibero/total)](https://github.com/voldemarpanso/ha_hailolibero/)
[![GitHub Last Commit](https://img.shields.io/github/last-commit/voldemarpanso/ha_hailolibero)](https://github.com/voldemarpanso/ha_hailolibero/)
[![HA Badge](https://img.shields.io/badge/Home%20Assistant-%23FFFFFF?logo=homeassistant)](https://www.home-assistant.io/)
[![HACS Badge](https://img.shields.io/badge/Custom-%2341BDF5?label=HACS)](https://hacs.xyz/docs/faq/custom_repositories/)
[![Static Badge](https://img.shields.io/badge/Buy%20me%20a%20beer-white?logo=paypal&label=Paypal)](https://www.paypal.com/donate/?business=KRHMM8QBFCVJ2&no_recurring=0&item_name=Buy+me+a+beer&currency_code=EUR)

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
