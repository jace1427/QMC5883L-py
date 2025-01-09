################
## CONSTANTS  ##
################
DFLT_BUS = 21
DFLT_ADDRESS = 0x0d

#### Registers ####
# Data Output
REG_XOUT_LSB = 0x00
REG_XOUT_MSB = 0x01
REG_YOUT_LSB = 0x02
REG_YOUT_MSB = 0x03
REG_ZOUT_LSB = 0x04
REG_ZOUT_MSB = 0x05

# Status
REG_STATUS_1 = 0x06

# Temperature Output
REG_TOUT_LSB = 0x07
REG_TOUT_MSB = 0x08

# Configuration
REG_CONTROL_1 = 0x09    # Control register 1
REG_CONTROL_2 = 0x0a    # Control register 2
REG_RST_PERIOD = 0x0b   # SET/RESET period register
REG_CHIP_ID = 0x0d      # ChipID register

#### Flags for status register 1 ####
STAT_DRDY = 0b00000001  # Data ready
STAT_OVL = 0b00000010   # Overflow
STAT_DOR = 0b00000100   # Data skipped for reading

#### Flags for control register 1 ####
# Mode control
MODE_STBY = 0b00000000  # Standby mode
MODE_CONT = 0b00000001  # Continuous read mode
# Output Data Rate
ODR_10HZ = 0b00000000
ODR_50HZ = 0b00000100
ODR_100HZ = 0b00001000
ODR_200HZ = 0b00001100
# Full scale
RNG_2G = 0b00000000     # Range 2 Gauss: for magnetic-clean environments
RNG_8G = 0b00010000     # Range 8 Gauss: for strong magnetic fields
# Over sample ratio
OSR_512 = 0b00000000    # 512: less noise, more power
OSR_256 = 0b01000000
OSR_128 = 0b10000000
OSR_64 = 0b11000000     # 64: more noise, less power

#### Flags for control register 2 ####
INT_ENB = 0b00000001    # Disable interrupt PIN
POL_PNT = 0b01000000    # Enable pointer roll-over function
SOFT_RST = 0b10000000   # Soft reset, restore default value of all registers


