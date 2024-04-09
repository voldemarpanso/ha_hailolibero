# Hailo Libero 3.0 Integration (non-official)
## Disclaimer
This is not official integration from Hailo. It's made out of curiosity, fun and beer.

## Supported device
- https://www.hailo.de/en/built-in-technology/p/hailo-libero-30-3697301

## Installation
- Add custom repo in HACS: https://github.com/voldemarpanso/ha_hailolibero

[![Open your Home Assistant instance and show the add add-on repository dialog with a specific repository URL pre-filled.](https://my.home-assistant.io/badges/supervisor_add_addon_repository.svg)](https://my.home-assistant.io/redirect/supervisor_add_addon_repository/?repository_url=https%3A%2F%2Fgithub.com%2Fvoldemarpanso%2Fha_hailolibero)

## Configuration
- Go to Settings -> Devices & Services
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
