
import smbus2

class QMC5883L():
    def __init__(self) -> None:
         pass

    def read(self):
        pass
#        """Read data from magnetic and temperature data registers."""
#        i = 0
#        [x, y, z, t] = [None, None, None, None]
#        while i < 20:  # Timeout after about 0.20 seconds.
#            status = self._read_byte(REG_STATUS_1)
#            if status & STAT_OVL:
#                # Some values have reached an overflow.
#                msg = ("Magnetic sensor overflow.")
#                if self.output_range == RNG_2G:
#                    msg += " Consider switching to RNG_8G output range."
#                logging.warning(msg)
#            if status & STAT_DOR:
#                # Previous measure was read partially, sensor in Data Lock.
#                x = self._read_word_2c(REG_XOUT_LSB)
#                y = self._read_word_2c(REG_YOUT_LSB)
#                z = self._read_word_2c(REG_ZOUT_LSB)
#                continue
#            if status & STAT_DRDY:
#                # Data is ready to read.
#                x = self._read_word_2c(REG_XOUT_LSB)
#                y = self._read_word_2c(REG_YOUT_LSB)
#                z = self._read_word_2c(REG_ZOUT_LSB)
#                t = self._read_word_2c(REG_TOUT_LSB)
#                break
#            else:
#                # Waiting for DRDY.
#                time.sleep(0.01)
#                i += 1
#        return [x, y, z, t]
#
if __name__ == '__main__':
    test = QMC5883L()
    print("hiya!")

