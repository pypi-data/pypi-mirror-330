# Welcome to SMfsrc’s documentation!

# Install

```bash
sudo pip install SMfsrc
```

or

```bash
sudo pip3 install SMfsrc
```

# Update

```bash
sudo pip install SMfsrc -U
```

or

```bash
sudo pip3 install SMfsrc -U
```

# Local Installation

```bash
git clone https://github.com/SequentMicrosystems/fsrc-rpi.git
cd ~/fsrc-rpi/python
sudo python setup.py install
```

# Initiate class

```console
$ python
Python 3.9.2 (default, Feb 28 2021, 17:03:44)
[GCC 10.2.1 20210110] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> import SMfsrc
>>> fsrc = SMfsrc.SMfsrc()
>>> fsrc.get_digi(1)
>>>
```

# Documentation

<a id="module-SMfsrc"></a>

### *class* SMfsrc.SMfsrc(stack=0, i2c=1)

Bases: `object`

Python class to control the Flagstaff-Research for Raspberry Pi.

* **Parameters:**
  * **stack** (*int*) – Stack level/device number.
  * **i2c** (*int*) – i2c bus number

#### get_all_digi()

Get all digital inputs status as a bitmask.

* **Returns:**
  (int) Digital bitmask

#### get_all_fets()

Get all fets state as bitmask.

* **Returns:**
  (int) Fets state bitmask

#### get_digi(channel)

Get digital input status.

* **Parameters:**
  **channel** (*int*) – Channel number
* **Returns:**
  (bool) Channel status

#### get_digi_counter(channel)

Get digital inputs counter for one channel.

* **Parameters:**
  **channel** (*int*) – Channel number
* **Returns:**
  (int) Digi counter

#### get_digi_edge(channel)

Get digital inputs counting edges status.

* **Parameters:**
  **channel** (*int*) – Channel number
* **Returns:**
  (int) Counting edge status
  : 0(none)/1(rising)/2(falling)/3(both)

#### get_fet(fet)

Get fet state.

* **Parameters:**
  **fet** (*int*) – Fet number
* **Returns:**
  (int) Fet state

#### get_owb_id(channel)

Get the 64bit ROM ID of the One Wire Bus connected sensor

* **Parameters:**
  **channel** (*int*) – Channel number
* **Returns:**
  (int) 64bit ROM ID

#### get_owb_no()

Get the number of Onw Wire Bus sensors connected

* **Returns:**
  (int) Number of sensors connected

#### get_owb_scan()

Start One Wire Bus scanning procedure.

#### get_owb_temp(channel)

Get the temperature from a one wire bus connected sensor.

* **Parameters:**
  **channel** (*int*) – Channel number
* **Returns:**
  (float) Temperature read from connected sensor

#### get_pump(channel)

Get pump value in %.

* **Parameters:**
  **channel** (*int*) – Channel number
* **Returns:**
  (float) Pump value in % for specified channel.

#### get_rtc()

Get rtc time.

* **Returns:**
  (tuple) date(year, month, day, hour, minute, second)

#### get_rtd_res(channel)

Get RTD resistance in ohm.

* **Parameters:**
  **channel** (*int*) – RTD channel number
* **Returns:**
  (float) RTD resistance value

#### get_rtd_temp(channel)

Get RTD temperature in Celsius.

* **Parameters:**
  **channel** (*int*) – RTD channel number
* **Returns:**
  (float) RTD Celsius value

#### get_u10_out(channel)

Get 0-10V output channel value in volts.

* **Parameters:**
  **channel** (*int*) – Channel number
* **Returns:**
  (float) 0-10V output value

#### get_u5_in(channel)

Get 0-5V input channel value in volts.

* **Parameters:**
  **channel** (*int*) – Channel number
* **Returns:**
  (float) Input value in volts

#### get_version()

Get firmware version.

Returns: (int) Firmware version number

#### reset_digi_counter(channel)

Reset digital inputs counter.

* **Parameters:**
  **channel** (*int*) – Channel number

#### set_all_fets(val)

Set all fets states as bitmask.

* **Parameters:**
  **val** (*int*) – Fets bitmask

#### set_digi_edge(channel, value)

Set digital inputs counting edges status.

* **Parameters:**
  * **channel** (*int*) – Channel number
  * **value** (*int*) – Counting edge status
    0(none)/1(rising)/2(falling)/3(both)

#### set_fet(fet, val)

Set fet state.

* **Parameters:**
  * **fet** (*int*) – Fet number
  * **val** – 0(OFF) or 1(ON)

#### set_pump(channel, value)

Set pump value in %.

* **Parameters:**
  * **channel** (*int*) – Channel number
  * **value** (*float*) – Pump value in %

#### set_pump_prescaler(value)

Set pump prescaler.

* **Parameters:**
  **value** (*int*) – Pump prescaler[0..65535]

#### set_rtc(year, month, day, hour, minute, second)

Set rtc time.

* **Parameters:**
  * **year** (*int*) – current year
  * **month** (*int*) – current month
  * **day** (*int*) – current day
  * **hour** (*int*) – current hour
  * **minute** (*int*) – current minute
  * **second** (*int*) – current second

#### set_u10_out(channel, value)

Set 0-10V output channel value in volts.

* **Parameters:**
  * **channel** (*int*) – Channel number
  * **value** (*float*) – Voltage value

#### wdt_clear_reset_count()

Clear watchdog counter.

#### wdt_get_init_period()

Get watchdog initial period.

* **Returns:**
  (int) Initial watchdog period in seconds

#### wdt_get_off_period()

Get watchdog off period in seconds.

* **Returns:**
  (int) Watchfog off period in seconds.

#### wdt_get_period()

Get watchdog period in seconds.

* **Returns:**
  (int) Watchdog period in seconds

#### wdt_get_reset_count()

Get watchdog reset count.

* **Returns:**
  (int) Watchdog reset count

#### wdt_reload()

Reload watchdog.

#### wdt_set_init_period(period)

Set watchdog initial period.

* **Parameters:**
  **period** (*int*) – Initial period in second

#### wdt_set_off_period(period)

Set off period in seconds

* **Parameters:**
  **period** (*int*) – Off period in seconds

#### wdt_set_period(period)

Set watchdog period.

* **Parameters:**
  **period** (*int*) – Channel number

<!-- vi:se ts=4 sw=4 et: -->
