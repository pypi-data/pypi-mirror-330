#!/usr/bin/python3

from smbus2 import SMBus
import struct
import datetime

import SMfsrc.fsrc_data as data
I2C_MEM = data.I2C_MEM
CHANNEL_NO = data.CHANNEL_NO

class SMfsrc: 
    """Python class to control the Flagstaff-Research for Raspberry Pi.

    Args:
        stack (int): Stack level/device number.
        i2c (int): i2c bus number
    """
    def __init__(self, stack=0, i2c=1):
        if stack < 0 or stack > data.STACK_LEVEL_MAX:
            raise ValueError("Invalid stack level!")
        self._hw_address_ = data.SLAVE_OWN_ADDRESS_BASE + stack
        self._i2c_bus_no = i2c
        self.bus = SMBus(self._i2c_bus_no)
        try:
            self._card_rev_major = self.bus.read_byte_data(self._hw_address_, I2C_MEM.REVISION_MAJOR)
            self._card_rev_minor = self.bus.read_byte_data(self._hw_address_, I2C_MEM.REVISION_MINOR)
        except Exception:
            print("{} not detected!".format(data.CARD_NAME))
            raise

    def _get_byte(self, address):
        return self.bus.read_byte_data(self._hw_address_, address)
    def _get_word(self, address):
        return self.bus.read_word_data(self._hw_address_, address)
    def _get_i16(self, address):
        buf = self.bus.read_i2c_block_data(self._hw_address_, address, 2)
        i16_value = struct.unpack("h", bytearray(buf))[0]
        return i16_value
    def _get_float(self, address):
        buf = self.bus.read_i2c_block_data(self._hw_address_, address, 4)
        float_value = struct.unpack("f", bytearray(buf))[0]
        return float_value
    def _get_i32(self, address):
        buf = self.bus.read_i2c_block_data(self._hw_address_, address, 4)
        i32_value = struct.unpack("i", bytearray(buf))[0]
        return i32_value
    def _get_u32(self, address):
        buf = self.bus.read_i2c_block_data(self._hw_address_, address, 4)
        u32_value = struct.unpack("I", bytearray(buf))[0]
        return u32_value
    def _get_u64(self, address):
        buf = self.bus.read_i2c_block_data(self._hw_address_, address, 8)
        u64_value = struct.unpack("Q", bytearray(buf))[0]
    def _get_block_data(self, address, byteno=4):
        return self.bus.read_i2c_block_data(self._hw_address_, address, byteno)
    def _set_byte(self, address, value):
        self.bus.write_byte_data(self._hw_address_, address, int(value))
    def _set_word(self, address, value):
        self.bus.write_word_data(self._hw_address_, address, int(value))
    def _set_float(self, address, value):
        ba = bytearray(struct.pack("f", value))
        self.bus.write_block_data(self._hw_address_, address, ba)
    def _set_i32(self, address, value):
        ba = bytearray(struct.pack("i", value))
        self.bus.write_block_data(self._hw_address_, address, ba)
    def _set_block(self, address, ba):
        self.bus.write_i2c_block_data(self._hw_address_, address, ba)

    @staticmethod
    def _check_channel(channel_type, channel):
        if not (0 <= channel and channel <= CHANNEL_NO[channel_type]):
            raise ValueError("Invalid {} channel number. Must be [1..{}]!".format(channel_type, CHANNEL_NO[channel_type]))
    def get_version(self):
        """Get firmware version.

        Returns: (int) Firmware version number
        """
        version_major = self._get_byte(I2C_MEM.REVISION_MAJOR)
        version_minor = self._get_byte(I2C_MEM.REVISION_MINOR)
        version = str(version_major) + "." + str(version_minor)
        return version

    def get_owb_temp(self, channel):
        """Get the temperature from a one wire bus connected sensor.

        Args:
            channel (int): Channel number

        Returns:
            (float) Temperature read from connected sensor
        """
        self._check_channel("owb", channel)
        dev = self._get_byte(I2C_MEM.OWB_DEV)
        if(not(1 <= channel and channel <= dev)):
            raise ValueError("Invalid channel number, only %d sensors connected".format(dev))
        value = self._get_word(I2C_MEM.OWB_TEMP + (channel - 1) * 2)
        return float(value) / 100

    def get_owb_scan(self):
        """Start One Wire Bus scanning procedure.
        """
        self._set_byte(I2C_MEM.OWB_START_SEARCH, 1)

    def get_owb_id(self, channel):
        """Get the 64bit ROM ID of the One Wire Bus connected sensor

        Args:
            channel (int): Channel number

        Returns:
            (int) 64bit ROM ID
        """
        dev = self._get_byte(I2C_MEM.OWB_DEV)
        if(not(1 <= channel and channel <= dev)):
            raise ValueError("Invalid channel number")
        self._set_byte(I2C_MEM.OWB_ROM_CODE_IDX, channel - 1)
        id = self._get_u64(I2C_MEM.OWB_ROM_CODE)
        return id

    def get_owb_no(self):
        """Get the number of Onw Wire Bus sensors connected

        Returns:
            (int) Number of sensors connected
        """
        no = self._get_byte(I2C_MEM.OWB_DEV)
        return no

    def get_fet(self, fet):
        """Get fet state.

        Args:
            fet (int): Fet number

        Returns:
            (int) Fet state
        """
        self._check_channel("fet", fet)
        val = self._get_byte(I2C_MEM.FETS)
        if (val & (1 << (fet - 1))) != 0:
            return 1
        return 0

    def get_all_fets(self):
        """Get all fets state as bitmask.

        Returns:
            (int) Fets state bitmask
        """
        val = self._get_byte(I2C_MEM.FETS)
        return val

    def set_fet(self, fet, val):
        """Set fet state.

        Args:
            fet (int): Fet number
            val: 0(OFF) or 1(ON)
        """
        self._check_channel("fet", fet)
        if val == 0:
            self._set_byte(I2C_MEM.FET_CLR, fet)
        elif val == 1:
            self._set_byte(I2C_MEM.FET_SET, fet)
        else:
            raise ValueError("Invalid fet value(0/1)")

    def set_all_fets(self, val):
        """Set all fets states as bitmask.

        Args:
            val (int): Fets bitmask
        """
        if(not (0 <= val and val <= (1 << CHANNEL_NO["fet"]) - 1)):
            raise ValueError("Invalid fet mask!")
        self._set_byte(I2C_MEM.FETS, 0xff & val)

    def get_u5_in(self, channel):
        """Get 0-5V input channel value in volts.

        Args:
            channel (int): Channel number

        Returns:
            (float) Input value in volts
        """
        self._check_channel("u5_in", channel)
        value = self._get_word(I2C_MEM.U5_IN + (channel - 1) * 2)
        return value / data.VOLT_TO_MILIVOLT

    def get_u10_out(self, channel):
        """Get 0-10V output channel value in volts.

        Args:
            channel (int): Channel number

        Returns:
            (float) 0-10V output value
        """
        self._check_channel("u10_out", channel)
        value = self._get_word(I2C_MEM.U10_OUT + (channel - 1) * 2)
        return value / data.VOLT_TO_MILIVOLT

    def set_u10_out(self, channel, value):
        """Set 0-10V output channel value in volts.

        Args:
            channel (int): Channel number
            value (float): Voltage value
        """
        self._check_channel("u10_out", channel)
        value = value * data.VOLT_TO_MILIVOLT
        self._set_word(I2C_MEM.U10_OUT + (channel - 1) * 2, value)

    def get_rtd_res(self, channel):
        """Get RTD resistance in ohm.

        Args:
            channel (int): RTD channel number

        Returns:
            (float) RTD resistance value
        """
        self._check_channel("rtd", channel)
        return self._get_float(I2C_MEM.RTD_RES + (channel - 1) * 4)
    def get_rtd_temp(self, channel):
        """Get RTD temperature in Celsius.

        Args:
            channel (int): RTD channel number

        Returns:
            (float) RTD Celsius value
        """
        self._check_channel("rtd", channel)
        return self._get_float(I2C_MEM.RTD_TEMP + (channel - 1) * 4)

    def wdt_reload(self):
        """Reload watchdog."""
        self._set_byte(I2C_MEM.WDT_RESET, data.WDT_RESET_SIGNATURE)
    def wdt_get_period(self):
        """Get watchdog period in seconds.

        Returns:
            (int) Watchdog period in seconds
        """
        return self._get_word(I2C_MEM.WDT_INTERVAL_GET)
    def wdt_set_period(self, period):
        """Set watchdog period.

        Args:
            period (int): Channel number
        """
        return self._set_word(I2C_MEM.WDT_INTERVAL_SET, period)
    def wdt_get_init_period(self):
        """Get watchdog initial period.

        Returns:
            (int) Initial watchdog period in seconds
        """
        return self._get_word(I2C_MEM.WDT_INIT_INTERVAL_GET)
    def wdt_set_init_period(self, period):
        """Set watchdog initial period.

        Args:
            period (int): Initial period in second
        """
        return self._set_word(I2C_MEM.WDT_INIT_INTERVAL_SET, period)

    def wdt_get_off_period(self):
        """Get watchdog off period in seconds.

        Returns:
            (int) Watchfog off period in seconds.
        """
        return self._get_i32(I2C_MEM.WDT_POWER_OFF_INTERVAL_GET)
    def wdt_set_off_period(self, period):
        """Set off period in seconds

        Args:
            period (int): Off period in seconds
        """
        return self._set_i32(I2C_MEM.WDT_POWER_OFF_INTERVAL_SET, period)
    def wdt_get_reset_count(self):
        """Get watchdog reset count.

        Returns:
            (int) Watchdog reset count
        """
        return self._get_word(I2C_MEM.WDT_RESET_COUNT)
    def wdt_clear_reset_count(self):
        """Clear watchdog counter. """
        return self._set_i32(I2C_MEM.WDT_CLEAR_RESET_COUNT, data.WDT_RESET_COUNT_SIGNATURE)

    def get_rtc(self):
        """Get rtc time.

        Returns:
            (tuple) date(year, month, day, hour, minute, second)
        """
        buf = self._get_block_data(I2C_MEM.RTC_YEAR, 6)
        buf[0] += 2000
        return tuple(buf)
    def set_rtc(self, year, month, day, hour, minute, second):
        """Set rtc time.

        Args:
            year (int): current year
            month (int): current month
            day (int): current day
            hour (int): current hour
            minute (int): current minute
            second (int): current second
        """
        if year > 2000:
            year -= 2000
        if(not(0 <= year and year <= 255)):
            raise ValueError("Invalid year!")
        datetime.datetime(
                year=2000+year, month=month, day=day,
                hour=hour, minute=minute, second=second)
        ba = bytearray(struct.pack(
            "6B B",
            year, month, day, hour, minute, second,
            data.CALIBRATION_KEY))
        self._set_block(I2C_MEM.RTC_SET_YEAR, ba)

    def get_digi(self, channel):
        """Get digital input status. 

        Args:
            channel (int): Channel number

        Returns:
            (bool) Channel status
        """
        self._check_channel("digi", channel)
        digi_mask = self._get_byte(I2C_MEM.DIGI)
        if(digi_mask & (1 << (channel - 1))):
            return True
        else:
            return False

    def get_all_digi(self):
        """Get all digital inputs status as a bitmask.

        Returns:
            (int) Digital bitmask
        """
        return self._get_byte(I2C_MEM.DIGI)
    def get_digi_edge(self, channel):
        """Get digital inputs counting edges status.

        Args:
            channel (int): Channel number

        Returns:
            (int) Counting edge status
                0(none)/1(rising)/2(falling)/3(both)
        """
        self._check_channel("digi", channel)
        rising = self._get_byte(I2C_MEM.DIGI_RISING)
        falling = self._get_byte(I2C_MEM.DIGI_FALLING)
        channel_bit = 1 << (channel - 1)
        value = 0
        if(rising & channel_bit):
            value |= 1
        if(falling & channel_bit):
            value |= 2
        return value

    def set_digi_edge(self, channel, value):
        """Set digital inputs counting edges status.

        Args:
            channel (int): Channel number
            value (int): Counting edge status
                0(none)/1(rising)/2(falling)/3(both)
        """
        self._check_channel("digi", channel)
        rising = self._get_byte(I2C_MEM.DIGI_RISING)
        falling = self._get_byte(I2C_MEM.DIGI_FALLING)
        channel_bit = 1 << (channel - 1)
        if(value & 1):
            rising |= channel_bit
        else:
            rising &= ~channel_bit
        if(value & 2):
            falling |= channel_bit
        else:
            rising &= ~channel_bit
        self._set_byte(I2C_MEM.DIGI_RISING, rising)
        self._set_byte(I2C_MEM.DIGI_FALLING, falling)
    def get_digi_counter(self, channel):
        """Get digital inputs counter for one channel.

        Args:
            channel (int): Channel number

        Returns:
            (int) Digi counter
        """
        self._check_channel("DIGI", channel)
        return self._get_u32(I2C_MEM.DIGI_COUNT + (channel - 1) * 4)

    def reset_digi_counter(self, channel):
        """Reset digital inputs counter.

        Args:
            channel (int): Channel number
        """
        self._check_channel("digi", channel)
        return self._set_byte(I2C_MEM.DIGI_COUNT_RST, channel)

    def get_pump(self, channel):
        """Get pump value in %.

        Args:
            channel (int): Channel number

        Returns:
            (float) Pump value in % for specified channel.
        """
        self._check_channel("pump", channel)
        return self._get_i16(I2C_MEM.PUMP + (channel - 1) * 2) / 10

    def set_pump(self, channel, value):
        """Set pump value in %.

        Args:
            channel (int): Channel number
            value (float): Pump value in %
        """
        self._check_channel("pump", channel)
        if(not(0 <= value and value <= 100)):
            raise ValueError("Pump value out of range! Must be [0..100]")
        self._set_word(I2C_MEM.PUMP + (channel - 1) * 2, value * 10)

    def set_pump_prescaler(self, value):
        """Set pump prescaler.

        Args:
            value (int): Pump prescaler[0..65535]
        """
        if(not(0 <= value and value <= 65535)):
            raise ValueError("Pump prescaler out of range! Must be [0..65535]")
        self._set_word(I2C_MEM.PUMP_PWM_PRESCALER, value)
