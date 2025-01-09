import logging
import time

from smbus2 import SMBus

import constants as c


class QMC5883L:
    def __init__(self, output_range=c.RNG_2G, address=c.DFLT_ADDRESS) -> None:
        self.bus = SMBus(1) # TODO - not sure why bus 1 but it seems right
        self.output_range = output_range
        self.addr = address

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
                time.sleep(0.01)
                i += 1
        print(f"X: {x}, Y: {y}, Z: {z}, T: {t},")
        return [x, y, z, t]


if __name__ == "__main__":
    compass = QMC5883L()
    compass.read()
