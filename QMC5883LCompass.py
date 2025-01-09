import logging
from time import sleep

from smbus2 import SMBus

import constants as c


class QMC5883L:
    def __init__(self, output_range=c.RNG_2G, address=c.DFLT_ADDRESS) -> None:
        self.bus = SMBus(c.DFLT_ADDRESS) # TODO - not sure why bus 1 but it seems right
        self.output_range = output_range
        self.addr = address
        self.mode_stby = (c.MODE_STBY | c.ODR_10HZ | c.RNG_2G | c.OSR_64)
        self.mode_cont = (c.MODE_CONT | c.ODR_10HZ | c.RNG_2G | c.OSR_512)

        chip_id = self.bus.read_byte_data(self.addr, c.REG_CHIP_ID)
        if chip_id != 0xff:
            msg = "Chip ID returned 0x%x instead of 0xff; is this the wrong chip?"
            logging.warning(msg, chip_id)

        self.mode_continuous()

    def __del__(self):
        self.mode_standby()

    def mode_continuous(self):
        self.bus.write_byte_data(self.addr, c.REG_CONTROL_2, c.SOFT_RST)  # Soft reset.
        self.bus.write_byte_data(self.addr, c.REG_CONTROL_2, c.INT_ENB)  # Disable interrupt.
        self.bus.write_byte_data(self.addr, c.REG_RST_PERIOD, 0x01)  # Define SET/RESET period.
        self.bus.write_byte_data(self.addr, c.REG_CONTROL_1, self.mode_cont)  # Set operation mode.

    def mode_standby(self):
        self.bus.write_byte_data(self.addr, c.REG_CONTROL_2, c.SOFT_RST)
        self.bus.write_byte_data(self.addr, c.REG_CONTROL_2, c.INT_ENB)
        self.bus.write_byte_data(self.addr, c.REG_RST_PERIOD, 0x01)
        self.bus.write_byte_data(self.addr, c.REG_CONTROL_1, self.mode_stby)

    def _read_data(self, low, high):
        low = self.bus.read_byte_data(self.addr, low)
        high = self.bus.read_byte_data(self.addr, high)
        ret = (high << 8) + low
        if ret >= 0x8000: 
            return ret - 0x10000
        else:
            return ret

    def read(self):
        """ """
        i = 20
        [x, y, z, t] = [None, None, None, None]
        while i < 20:  # Timeout after about 0.20 seconds.
            status = self.bus.read_byte_data(self.addr, c.REG_STATUS_1)
            if status & c.STAT_OVL:
                # Some values have reached an overflow.
                msg = "Magnetic sensor overflow."
                if self.output_range == c.RNG_2G:
                    msg += " Consider switching to RNG_8G output range."
                logging.warning(msg)
            if status & c.STAT_DOR:
                # Previous measure was read partially, sensor in Data Lock.
                x = self._read_data(c.REG_XOUT_LSB, c.REG_XOUT_MSB)
                y = self._read_data(c.REG_YOUT_LSB, c.REG_YOUT_MSB)
                z = self._read_data(c.REG_ZOUT_LSB, c.REG_ZOUT_MSB)
                continue
            if status & c.STAT_DRDY:
                # Data is ready to read.
                x = self._read_data(c.REG_XOUT_LSB, c.REG_XOUT_MSB)
                y = self._read_data(c.REG_YOUT_LSB, c.REG_YOUT_MSB)
                z = self._read_data(c.REG_ZOUT_LSB, c.REG_ZOUT_MSB)
                t = self._read_data(c.REG_TOUT_LSB, c.REG_TOUT_MSB)
                break
            else:
                # Waiting for DRDY.
                sleep(0.01)
                i += 1
        print(f"X: {x}, Y: {y}, Z: {z}, T: {t},")
        return [x, y, z, t]


if __name__ == "__main__":
    compass = QMC5883L()
    for _ in range(1000):
        compass.read()

