# Naturela Smart Boiler for Home Assistant
An unofficial Home Assistant custom integration for cloud-connected Naturela Smart Boiler units, including Metalac models. It connects through a Naturela Smart Home account and lets Home Assistant monitor the boiler and send control commands.
This is a community-tested integration. It has been exercised with a Metalac boiler using an NHC-57 controller and software version 52. Other boiler/controller combinations still need user testing.
## Features
- View current water temperature and set the target temperature in whole 1 °C steps.
- Choose the boiler operation mode: Off, Heating, Smart, Self Learning, or Timer.
- Turn the Boiler Boost heater switch on or off.
- View daily/night energy use, saved energy, eco index, and error code sensors.
Mode changes and Boost control send commands through the Naturela cloud service. After changing a mode, check the status in Naturela Smart Home and confirm the boiler is behaving as expected.
## Installation with HACS
1. In Home Assistant, open **HACS → Integrations → ⋮ → Custom repositories**.
2. Add `https://github.com/LjubasDev/NaturelaBoilerMetalac` and choose **Integration** as the category.
3. Find **Naturela Smart Boiler**, download it, and restart Home Assistant.
4. Go to **Settings → Devices & services → Add integration** and search for **Naturela Smart Boiler**.
5. Enter the email and password for your Naturela Smart Home account and the boiler's device ID. The device ID is the number shown in the device page URL after `/smartboiler/`.
For manual installation, copy `custom_components/naturela_smartboiler` into the Home Assistant configuration directory at `custom_components/naturela_smartboiler`, then restart Home Assistant and add the integration as above.
## Entities in Home Assistant
The integration creates these entities under the Naturela Smart Boiler device:
- **Smart Boiler** (`water_heater`): current water temperature and target temperature.
- **Mode** (`select`): choose Off, Heating, Smart, Self Learning, or Timer. Add this entity to a dashboard to change the mode there.
- **Boiler Boost** (`switch`): manually control the heater element.
- Sensors for water temperature, daily and night energy, saved energy, eco index, and error code.
The entity ID can differ if another entity already uses the same name. Select the entity by its **Naturela Smart Boiler** device and friendly name.
## Report an issue or share test results
Please report problems or successful tests in [GitHub Issues](https://github.com/LjubasDev/NaturelaBoilerMetalac/issues). Include:
- Home Assistant Core version and integration version/commit.
- Boiler model, controller model, and controller software version, if known.
- The entity and command or mode you tried, plus the approximate time.
- What you expected and what actually happened.
- Relevant Home Assistant log lines with passwords, tokens, email addresses, and device identifiers removed.
Testing on more Naturela and Metalac models is welcome. Please never post your Naturela password, login tokens, or unredacted diagnostics.
