#!/usr/bin/python3
"""
__init__.py
This module provides the SM24b8vin class which implements the functionality
(for analog input, LED control, RTC, watchdog, and calibration)
of the 24b8vin card.
"""

from smbus2 import SMBus
import struct
import datetime

# Import the data definitions.
# (If you encounter issues with a module name starting with a digit,
# consider renaming “24b8vin_data.py” to, for example, “vin24b8_data.py”.)
from . import _24b8vin_data as data


class SM24b8vin:
    """
    Python class to control the 24b8vin card (Eight 24-bit analog inputs).
    
    This class provides methods to read the eight analog input channels,
    set/read the gain codes, control 8 LEDs, access the RTC, use the watchdog,
    and perform calibration operations.
    
    Args:
        stack (int): The device stack index (added to SLAVE_OWN_ADDRESS_BASE).
        i2c (int): I2C bus number.
    """
    def __init__(self, stack=0, i2c=1):
        self._hw_address = data.SLAVE_OWN_ADDRESS_BASE + stack
        self._i2c_bus_no = i2c
        self.bus = SMBus(self._i2c_bus_no)
        try:
            self._card_rev_major = self.bus.read_byte_data(
                self._hw_address, data.I2C_MEM.REVISION_HW_MAJOR_ADD)
            self._card_rev_minor = self.bus.read_byte_data(
                self._hw_address, data.I2C_MEM.REVISION_HW_MINOR_ADD)
        except Exception as e:
            print("{} not detected!".format(data.CARD_NAME))
            raise e

    # --- Low–level I2C access methods ---
    def _get_byte(self, address):
        return self.bus.read_byte_data(self._hw_address, address)

    def _get_word(self, address):
        return self.bus.read_word_data(self._hw_address, address)

    def _get_i16(self, address):
        buf = self.bus.read_i2c_block_data(self._hw_address, address, 2)
        return struct.unpack("h", bytearray(buf))[0]

    def _get_i32(self, address):
        buf = self.bus.read_i2c_block_data(self._hw_address, address, 4)
        return struct.unpack("i", bytearray(buf))[0]

    def _get_u32(self, address):
        buf = self.bus.read_i2c_block_data(self._hw_address, address, 4)
        return struct.unpack("I", bytearray(buf))[0]

    def _get_float(self, address):
        buf = self.bus.read_i2c_block_data(self._hw_address, address, 4)
        return struct.unpack("f", bytearray(buf))[0]

    def _get_block_data(self, address, length):
        return self.bus.read_i2c_block_data(self._hw_address, address, length)

    def _set_byte(self, address, value):
        self.bus.write_byte_data(self._hw_address, address, int(value))

    def _set_word(self, address, value):
        self.bus.write_word_data(self._hw_address, address, int(value))

    def _set_float(self, address, value):
        ba = list(bytearray(struct.pack("f", value)))
        self.bus.write_i2c_block_data(self._hw_address, address, ba)

    def _set_i32(self, address, value):
        ba = list(bytearray(struct.pack("i", value)))
        self.bus.write_i2c_block_data(self._hw_address, address, ba)

    def _set_block(self, address, ba):
        self.bus.write_i2c_block_data(self._hw_address, address, list(ba))

    # --- High–level methods ---

    # Analog inputs (24–bit floating point values)
    def get_u_in(self, channel):
        """
        Get analog input voltage for a given channel (in volts).
        
        Args:
            channel (int): Channel number [1..{u_in}].
        
        Returns:
            float: Voltage value in volts.
        """
        if not (1 <= channel <= data.CHANNEL_NO["u_in"]):
            raise ValueError("Invalid u_in channel number. Must be 1-{}."
                             .format(data.CHANNEL_NO["u_in"]))
        addr = data.I2C_MEM.U_IN_VAL1_ADD + (channel - 1) * data.ANALOG_VAL_SIZE
        return self._get_float(addr)

    # Gain codes (one byte per channel)
    def get_gain(self, channel):
        """
        Get gain setting for an analog input channel.
        
        Args:
            channel (int): Channel number [1..{gain}].
        
        Returns:
            int: Gain code.
        """
        if not (1 <= channel <= data.CHANNEL_NO["gain"]):
            raise ValueError("Invalid gain channel number. Must be 1-{}."
                             .format(data.CHANNEL_NO["gain"]))
        addr = data.I2C_MEM.GAIN_CH1 + (channel - 1)
        return self._get_byte(addr)

    def set_gain(self, channel, gain):
        """
        Set the gain for an analog input channel.
        
        Args:
            channel (int): Channel number [1..{gain}].
            gain (int): Gain code (0–7).
        """
        if not (1 <= channel <= data.CHANNEL_NO["gain"]):
            raise ValueError("Invalid gain channel number. Must be 1-{}."
                             .format(data.CHANNEL_NO["gain"]))
        if not (0 <= gain <= 7):
            raise ValueError("Invalid gain value. Must be between 0 and 7.")
        addr = data.I2C_MEM.GAIN_CH1 + (channel - 1)
        self._set_byte(addr, gain)

    # LED methods
    def get_led(self, led):
        """
        Get the state of a single LED.
        
        Args:
            led (int): LED number [1..{led}].
        
        Returns:
            int: 1 (ON) or 0 (OFF).
        """
        if not (1 <= led <= data.CHANNEL_NO["led"]):
            raise ValueError("Invalid LED channel. Must be 1-{}."
                             .format(data.CHANNEL_NO["led"]))
        val = self._get_byte(data.I2C_MEM.LEDS)
        return 1 if (val & (1 << (led - 1))) else 0

    def get_all_leds(self):
        """
        Get the status of all LEDs as a bitmask.
        
        Returns:
            int: Bitmask of LED states.
        """
        return self._get_byte(data.I2C_MEM.LEDS)

    def set_led(self, led, state):
        """
        Set the state of a single LED.
        
        Args:
            led (int): LED number [1..{led}].
            state (int): 0 (OFF) or 1 (ON).
        """
        if not (1 <= led <= data.CHANNEL_NO["led"]):
            raise ValueError("Invalid LED channel. Must be 1-{}."
                             .format(data.CHANNEL_NO["led"]))
        if state not in (0, 1):
            raise ValueError("Invalid LED state. Must be 0 or 1.")
        if state == 1:
            self._set_byte(data.I2C_MEM.LED_SET, led)
        else:
            self._set_byte(data.I2C_MEM.LED_CLR, led)

    def set_all_leds(self, bitmask):
        """
        Set all LEDs at once using a bitmask.
        
        Args:
            bitmask (int): Bitmask value (0 to 2^(LED_CH_NO)-1).
        """
        if not (0 <= bitmask < (1 << data.CHANNEL_NO["led"])):
            raise ValueError("Invalid LED bitmask.")
        self._set_byte(data.I2C_MEM.LEDS, bitmask)

    # RTC methods
    def get_rtc(self):
        """
        Get the real–time clock (RTC) time.
        
        Returns:
            tuple: (year, month, day, hour, minute, second)
        """
        buf = self._get_block_data(data.I2C_MEM.RTC_YEAR_ADD, 6)
        buf[0] += 2000
        return tuple(buf)

    def set_rtc(self, year, month, day, hour, minute, second):
        """
        Set the RTC time.
        
        Args:
            year (int): Full year (e.g. 2025)
            month, day, hour, minute, second (int): Date/time components.
        """
        if year >= 2000:
            year -= 2000
        # Validate date/time by attempting to create a datetime object
        datetime.datetime(2000 + year, month, day, hour, minute, second)
        ba = list(bytearray(struct.pack("6B", year, month, day, hour, minute, second)))
        # Append the calibration key as required by the protocol
        ba.append(data.CALIBRATION_KEY)
        self._set_block(data.I2C_MEM.RTC_SET_YEAR_ADD, ba)

    # Watchdog Timer (WDT) methods
    def wdt_reload(self):
        """Reload (reset) the watchdog timer."""
        self._set_byte(data.I2C_MEM.MEM_WDT_RESET_ADD, data.WDT_RESET_SIGNATURE)

    def wdt_get_period(self):
        """Get the watchdog period (in seconds)."""
        return self._get_word(data.I2C_MEM.MEM_WDT_INTERVAL_GET_ADD)

    def wdt_set_period(self, period):
        """
        Set the watchdog period.
        
        Args:
            period (int): Period in seconds.
        """
        self._set_word(data.I2C_MEM.MEM_WDT_INTERVAL_SET_ADD, period)

    def wdt_get_init_period(self):
        """Get the initial watchdog period (in seconds)."""
        return self._get_word(data.I2C_MEM.MEM_WDT_INIT_INTERVAL_GET_ADD)

    def wdt_set_init_period(self, period):
        """
        Set the initial watchdog period.
        
        Args:
            period (int): Period in seconds.
        """
        self._set_word(data.I2C_MEM.MEM_WDT_INIT_INTERVAL_SET_ADD, period)

    def wdt_get_off_period(self):
        """Get the watchdog power–off period (in seconds)."""
        return self._get_i32(data.I2C_MEM.MEM_WDT_POWER_OFF_INTERVAL_GET_ADD)

    def wdt_set_off_period(self, period):
        """
        Set the watchdog power–off period.
        
        Args:
            period (int): Off period in seconds.
        """
        self._set_i32(data.I2C_MEM.MEM_WDT_POWER_OFF_INTERVAL_SET_ADD, period)

    def wdt_get_reset_count(self):
        """Get the watchdog reset count."""
        return self._get_word(data.I2C_MEM.MEM_WDT_RESET_COUNT_ADD)

    def wdt_clear_reset_count(self):
        """Clear the watchdog reset count."""
        self._set_i32(data.I2C_MEM.MEM_WDT_CLEAR_RESET_COUNT_ADD, data.WDT_RESET_COUNT_SIGNATURE)

    # Revision/version information
    def get_version(self):
        """
        Get the firmware version.
        
        Returns:
            str: Version string in the form "major.minor".
        """
        ver_major = self._get_byte(data.I2C_MEM.REVISION_MAJOR_ADD)
        ver_minor = self._get_byte(data.I2C_MEM.REVISION_MINOR_ADD)
        return "{}.{}".format(ver_major, ver_minor)
