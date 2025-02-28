# Welcome to SM24b8vin’s documentation!

# Install

```bash
sudo pip install SM24b8vin
```

or

```bash
sudo pip3 install SM24b8vin
```

# Update

```bash
sudo pip install SM24b8vin -U
```

or

```bash
sudo pip3 install SM24b8vin -U
```

# Initiate class

```console
$ python
Python 3.11.8 (main, Feb 12 2024, 14:50:05) [GCC 13.2.1 20230801] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> import SM24b8vin
>>> sm24b = SM24b8vin.SM24b8vin()
>>> sm24b.get_u_in(1)
>>>
```

# Documentation

<a id="module-SM24b8vin"></a>

\_\_init_\_.py
This module provides the SM24b8vin class which implements the functionality
(for analog input, LED control, RTC, watchdog, and calibration)
of the 24b8vin card.

### *class* SM24b8vin.SM24b8vin(stack=0, i2c=1)

Bases: `object`

Python class to control the 24b8vin card (Eight 24-bit analog inputs).

This class provides methods to read the eight analog input channels,
set/read the gain codes, control 8 LEDs, access the RTC, use the watchdog,
and perform calibration operations.

* **Parameters:**
  * **stack** (*int*) – The device stack index (added to SLAVE_OWN_ADDRESS_BASE).
  * **i2c** (*int*) – I2C bus number.

#### get_all_leds()

Get the status of all LEDs as a bitmask.

* **Returns:**
  Bitmask of LED states.
* **Return type:**
  int

#### get_gain(channel)

Get gain setting for an analog input channel.

* **Parameters:**
  **channel** (*int*) – Channel number [1..{gain}].
* **Returns:**
  Gain code.
* **Return type:**
  int

#### get_led(led)

Get the state of a single LED.

* **Parameters:**
  **led** (*int*) – LED number [1..{led}].
* **Returns:**
  1 (ON) or 0 (OFF).
* **Return type:**
  int

#### get_rtc()

Get the real–time clock (RTC) time.

* **Returns:**
  (year, month, day, hour, minute, second)
* **Return type:**
  tuple

#### get_u_in(channel)

Get analog input voltage for a given channel (in volts).

* **Parameters:**
  **channel** (*int*) – Channel number [1..{u_in}].
* **Returns:**
  Voltage value in volts.
* **Return type:**
  float

#### get_version()

Get the firmware version.

* **Returns:**
  Version string in the form “major.minor”.
* **Return type:**
  str

#### set_all_leds(bitmask)

Set all LEDs at once using a bitmask.

* **Parameters:**
  **bitmask** (*int*) – Bitmask value (0 to 2^(LED_CH_NO)-1).

#### set_gain(channel, gain)

Set the gain for an analog input channel.

* **Parameters:**
  * **channel** (*int*) – Channel number [1..{gain}].
  * **gain** (*int*) – Gain code (0–7).

#### set_led(led, state)

Set the state of a single LED.

* **Parameters:**
  * **led** (*int*) – LED number [1..{led}].
  * **state** (*int*) – 0 (OFF) or 1 (ON).

#### set_rtc(year, month, day, hour, minute, second)

Set the RTC time.

* **Parameters:**
  * **year** (*int*) – Full year (e.g. 2025)
  * **month** (*int*) – Date/time components.
  * **day** (*int*) – Date/time components.
  * **hour** (*int*) – Date/time components.
  * **minute** (*int*) – Date/time components.
  * **second** (*int*) – Date/time components.

#### wdt_clear_reset_count()

Clear the watchdog reset count.

#### wdt_get_init_period()

Get the initial watchdog period (in seconds).

#### wdt_get_off_period()

Get the watchdog power–off period (in seconds).

#### wdt_get_period()

Get the watchdog period (in seconds).

#### wdt_get_reset_count()

Get the watchdog reset count.

#### wdt_reload()

Reload (reset) the watchdog timer.

#### wdt_set_init_period(period)

Set the initial watchdog period.

* **Parameters:**
  **period** (*int*) – Period in seconds.

#### wdt_set_off_period(period)

Set the watchdog power–off period.

* **Parameters:**
  **period** (*int*) – Off period in seconds.

#### wdt_set_period(period)

Set the watchdog period.

* **Parameters:**
  **period** (*int*) – Period in seconds.

<!-- vi:se ts=4 sw=4 et: -->
