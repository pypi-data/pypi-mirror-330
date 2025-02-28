"""
24b8vin_data.py
This file defines the constants and “enum‐like” types used by the 24b8vin card.
Based on the C header “data.h”.
"""

# Card identification
CARD_NAME = "Eight 24-Bit Analog Inputs"
PROGRAM_NAME = "24b8vin"

# I2C addressing and firmware/hardware revisions
SLAVE_OWN_ADDRESS_BASE = 0x31

HW_MAJOR = 1
HW_MINOR = 0
FW_MAJOR = 1
FW_MINOR = 1
VERSION = "1.0"

# Channel definitions
U_IN_CH_NO = 8
ANALOG_VAL_SIZE = 4
MODBUS_SETTINGS_SIZE_B = 5

MIN_CH_NO = 1
LED_CH_NO = 8

VOLT_TO_MILIVOLT = 1000

# Calibration keys
CALIBRATION_KEY = 0xaa
RESET_CALIBRATION_KEY = 0x55

# Watchdog signatures
WDT_RESET_SIGNATURE = 0xca
WDT_RESET_COUNT_SIGNATURE = 0xbe

# Calibration point IDs (for outputs, if needed)
CAL_0_10V_OUT_START_ID = 6
CAL_0_10V_OUT_STOP_ID  = 7
CAL_4_20mA_OUT_START_ID = 8
CAL_4_20mA_OUT_STOP_ID  = 9

# Calibration status (enum from data.h)
CALIB_IN_PROGRESS = 0
CALIB_DONE        = 1
CALIB_ERROR       = 2

# Calibration channels (data.h only defines one calibratable channel)
CALIB_CH_NONE  = 0
CALIB_U_IN_CH1 = 1

#
# I2C memory map
#
# (Some addresses are computed from U_IN_CH_NO, ANALOG_VAL_SIZE, etc.)
#
class I2C_MEM:
    # LED related registers (8 LEDs)
    LEDS    = 0
    LED_SET = 1
    LED_CLR = 2

    # Analog inputs:
    # Eight 4‐byte floating–point values (expressed in Volts)
    U_IN_VAL1_ADD = 3
    MEM_U_IN      = U_IN_VAL1_ADD  # Alias

    # Gain settings for the eight channels.
    # The first gain code is located at:
    GAIN_CH1 = U_IN_VAL1_ADD + U_IN_CH_NO * ANALOG_VAL_SIZE  # 3 + 8*4 = 35

    # Diagnostic registers:
    MEM_DIAG_TEMPERATURE_ADD = GAIN_CH1 + U_IN_CH_NO  # 35 + 8 = 43
    MEM_DIAG_RASP_V_ADD      = MEM_DIAG_TEMPERATURE_ADD + 1   # 44
    MEM_DIAG_RASP_V          = MEM_DIAG_RASP_V_ADD + 1          # 45
    MEM_DIAG_RASP_V1         = MEM_DIAG_RASP_V + 1              # 46

    # RTC registers:
    RTC_YEAR_ADD       = MEM_DIAG_RASP_V1 + 1  # 47
    RTC_MONTH_ADD      = RTC_YEAR_ADD + 1       # 48
    RTC_DAY_ADD        = RTC_MONTH_ADD + 1      # 49
    RTC_HOUR_ADD       = RTC_DAY_ADD + 1        # 50
    RTC_MINUTE_ADD     = RTC_HOUR_ADD + 1       # 51
    RTC_SECOND_ADD     = RTC_MINUTE_ADD + 1     # 52
    RTC_SET_YEAR_ADD   = RTC_SECOND_ADD + 1     # 53
    RTC_SET_MONTH_ADD  = RTC_SET_YEAR_ADD + 1     # 54
    RTC_SET_DAY_ADD    = RTC_SET_MONTH_ADD + 1    # 55
    RTC_SET_HOUR_ADD   = RTC_SET_DAY_ADD + 1      # 56
    RTC_SET_MINUTE_ADD = RTC_SET_HOUR_ADD + 1     # 57
    RTC_SET_SECOND_ADD = RTC_SET_MINUTE_ADD + 1   # 58
    RTC_CMD_ADD        = RTC_SET_SECOND_ADD + 1   # 59

    # Watchdog Timer registers:
    MEM_WDT_RESET_ADD               = RTC_CMD_ADD + 1           # 60
    MEM_WDT_INTERVAL_SET_ADD        = MEM_WDT_RESET_ADD + 1     # 61
    MEM_WDT_INTERVAL_GET_ADD        = MEM_WDT_INTERVAL_SET_ADD + 2  # 63
    MEM_WDT_INIT_INTERVAL_SET_ADD   = MEM_WDT_INTERVAL_GET_ADD + 2  # 65
    MEM_WDT_INIT_INTERVAL_GET_ADD   = MEM_WDT_INIT_INTERVAL_SET_ADD + 2  # 67
    MEM_WDT_RESET_COUNT_ADD         = MEM_WDT_INIT_INTERVAL_GET_ADD + 2  # 69
    MEM_WDT_CLEAR_RESET_COUNT_ADD   = MEM_WDT_RESET_COUNT_ADD + 2  # 71
    MEM_WDT_POWER_OFF_INTERVAL_SET_ADD = MEM_WDT_CLEAR_RESET_COUNT_ADD + 1  # 72
    MEM_WDT_POWER_OFF_INTERVAL_GET_ADD = MEM_WDT_POWER_OFF_INTERVAL_SET_ADD + 4  # 76
    MEM_BUTTON                    = MEM_WDT_POWER_OFF_INTERVAL_GET_ADD + 4   # 80

    # Modbus settings
    MODBUS_SETINGS_ADD = MEM_BUTTON + 1  # 81

    # Calibration registers:
    MEM_CALIB_VALUE   = MODBUS_SETINGS_ADD + MODBUS_SETTINGS_SIZE_B  # 81 + 5 = 86
    MEM_CALIB_CHANNEL = MEM_CALIB_VALUE + 4   # 86 + 4 = 90
    MEM_CALIB_KEY     = MEM_CALIB_CHANNEL + 1     # 91
    MEM_CALIB_STATUS  = MEM_CALIB_KEY + 1         # 92

    # Update register:
    MEM_UPDATE_ADD = 0xaa  # 170

    # Revision registers:
    REVISION_HW_MAJOR_ADD = 251
    REVISION_HW_MINOR_ADD = REVISION_HW_MAJOR_ADD + 1  # 252
    REVISION_MAJOR_ADD    = REVISION_HW_MINOR_ADD + 1   # 253
    REVISION_MINOR_ADD    = REVISION_MAJOR_ADD + 1      # 254

    SLAVE_BUFF_SIZE = 255

# Error codes
ERROR         = -1
OK            = 0
ARG_CNT_ERR   = -2
ARG_RANGE_ERROR = -3
IO_ERROR      = -4

# Some mask definitions (useful for bit–manipulation)
MASK_1 = 1
MASK_2 = 3
MASK_3 = 7
MASK_4 = 15
MASK_5 = 31
MASK_6 = 63
MASK_7 = 127

def MASK(x):
    """Return a mask of x ones (for 1 <= x <= 7)."""
    if 1 <= x <= 7:
        return (1 << x) - 1
    else:
        raise ValueError("Invalid mask parameter: {}".format(x))

# State (for example LED or digital output states)
class State:
    OFF = 0
    ON  = 1
    STATE_COUNT = 2

# Channel numbers (for range checking)
CHANNEL_NO = {
    "u_in": U_IN_CH_NO,
    "led": LED_CH_NO,
    "gain": U_IN_CH_NO,
}
