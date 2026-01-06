# test_sundatetime.py

import unittest
from datetime import datetime, timedelta, timezone
from tests import *

from suntime.sundatetime import Sundatetime

class Tz(timezone):
    def __init__(self, hours: int, dst: int=0) -> None:
        super().__init__(timedelta(hours=hours))
        self._dst = dst

    def utcoffset(self, dt: datetime) -> timedelta:
        return super().utcoffset(dt) + self.dst(dt)

    def fromutc(self, dt: datetime) -> datetime:
        assert dt.tzinfo is self
        dt += self.utcoffset(dt)
        return dt.replace()

    def dst(self, dt: datetime) -> timedelta:
        return timedelta(hours=self._dst) if self.isdst(dt) else timedelta(0)

    def isdst(self, dt: datetime) -> bool:
        return self._dst != 0


class TestSunDatetime(unittest.TestCase):

    def test_sundatetime1(self):
        tz = Tz(tz1[0])
        sd1 = Sundatetime(*pl1)
        sd1.calc_sunrise_sunset(datetime(*dt1, tzinfo=tz))
        self.assertEqual(sd1.sunrise.tuple(),   (2000, 1, 1,  7, 40, 0, 0, tz, 0))
        self.assertEqual(sd1.sunset .tuple(),   (2000, 1, 1, 16, 47, 0, 0, tz, 0))
        self.assertFalse(sd1.is_daytime(datetime(2000, 1, 1,  0,  0, 0, 0, tz)))
        self.assertTrue (sd1.is_daytime(datetime(2000, 1, 1, 12,  0, 0, 0, tz)))
        self.assertTrue (sd1.is_sunrise(datetime(2000, 1, 1,  7, 40, 0, 0, tz)))
        self.assertTrue (sd1.is_sunset (datetime(2000, 1, 1, 16, 47, 0, 0, tz)))

    def test_sundatetime2(self):
        tz = Tz(tz2[0])
        sd2 = Sundatetime(*pl2)
        sd2.calc_sunrise_sunset(datetime(*dt2, tzinfo=tz))
        self.assertEqual(sd2.sunrise.tuple(),   (2014, 10, 3,  7, 16, 0, 0, tz, 0))
        self.assertEqual(sd2.sunset .tuple(),   (2014, 10, 3, 18, 46, 0, 0, tz, 0))
        self.assertFalse(sd2.is_daytime(datetime(2014, 10, 3,  0,  0, 0, 0, tz)))
        self.assertTrue (sd2.is_daytime(datetime(2014, 10, 3, 12,  0, 0, 0, tz)))
        self.assertTrue (sd2.is_sunrise(datetime(2014, 10, 3,  7, 16, 0, 0, tz)))
        self.assertTrue (sd2.is_sunset (datetime(2014, 10, 3, 18, 46, 0, 0, tz)))

    def test_sundatetime3(self):
        tz = Tz(tz3[0])
        sd3 = Sundatetime(*pl3)
        sd3.calc_sunrise_sunset(datetime(*dt3, tzinfo=tz))
        self.assertEqual(sd3.sunrise.tuple(),   (2016, 12, 21,  5, 32, 0, 0, tz, 0))
        self.assertEqual(sd3.sunset .tuple(),   (2016, 12, 21, 19, 57, 0, 0, tz, 0))
        self.assertFalse(sd3.is_daytime(datetime(2016, 12, 21,  0,  0, 0, 0, tz)))
        self.assertTrue (sd3.is_daytime(datetime(2016, 12, 21, 12,  0, 0, 0, tz)))
        self.assertTrue (sd3.is_sunrise(datetime(2016, 12, 21,  5, 32, 0, 0, tz)))
        self.assertTrue (sd3.is_sunset (datetime(2016, 12, 21, 19, 57, 0, 0, tz)))

    def test_sundatetime4(self):
        tz = Tz(tz4[0])
        sd4 = Sundatetime(*pl4)
        sd4.calc_sunrise_sunset(datetime(*dt4, tzinfo=tz))
        self.assertEqual(sd4.sunrise.tuple(),   (2021, 4, 23, 23,  4, 0, 0, tz, 0))
        self.assertEqual(sd4.sunset .tuple(),   (2021, 4, 24, 13, 49, 0, 0, tz, 0))

    def test_sundatetime5(self):
        tz = Tz(tz5[0])
        sd5 = Sundatetime(*pl5)
        sd5.calc_sunrise_sunset(datetime(*dt5, tzinfo=tz))
        self.assertEqual(sd5.sunrise.tuple(),     (2040, 8, 24, 12, 57, 0, 0, tz, 0))
        self.assertEqual(sd5.sunset .tuple(),     (2040, 8, 26, 12, 57, 0, 0, tz, 0))
        self.assertTrue (sd5.is_daytime  (datetime(2040, 8, 25,  0,  0, 0, 0, tz)))
        self.assertFalse(sd5.is_nighttime(datetime(2040, 8, 25, 12,  0, 0, 0, tz)))
        self.assertTrue (sd5.is_sunrise  (datetime(2040, 8, 24, 12, 57, 0, 0, tz)))
        self.assertTrue (sd5.is_sunset   (datetime(2040, 8, 26, 12, 57, 0, 0, tz)))

    def test_sundatetime6(self):
        tz = Tz(tz6[0])
        sd6 = Sundatetime(*pl6)
        sd6.calc_sunrise_sunset(datetime(*dt6, tzinfo=tz))
        self.assertEqual(sd6.sunrise.tuple(),   (2040, 8, 26, 1, 35, 0, 0, tz, 0))
        self.assertEqual(sd6.sunset .tuple(),   (2040, 8, 27, 0, 18, 0, 0, tz, 0))
        self.assertTrue (sd6.is_sunrise(datetime(2040, 8, 26, 1, 35, 0, 0, tz)))
        self.assertTrue (sd6.is_sunset (datetime(2040, 8, 27, 0, 18, 0, 0, tz)))

    def test_sundatetime7(self):
        tz = Tz(tz7[0])
        sd7 = Sundatetime(*pl7)
        sd7.calc_sunrise_sunset(datetime(*dt7, tzinfo=tz))
        self.assertEqual(sd7.sunrise.tuple(),     (2033, 8, 11, 13, 0, 0, 0, tz, 0))
        self.assertEqual(sd7.sunset .tuple(),     (2033, 8,  9, 13, 0, 0, 0, tz, 0))
        self.assertFalse(sd7.is_daytime  (datetime(2033, 8, 11, 12, 0, 0, 0, tz)))
        self.assertFalse(sd7.is_nighttime(datetime(2033, 8, 25,  0, 0, 0, 0, tz)))
        self.assertFalse(sd7.is_sunrise  (datetime(2033, 8, 11, 13, 0, 0, 0, tz)))
        self.assertFalse(sd7.is_sunset   (datetime(2033, 8,  9, 13, 0, 0, 0, tz)))

    def test_sundatetime8(self):
        tz = Tz(tz8[0])
        sd8 = Sundatetime(*pl8)
        sd8.calc_sunrise_sunset(datetime(*dt8, tzinfo=tz))
        self.assertEqual(sd8.sunrise.tuple(),     (2033, 10, 21,  3,  6, 0, 0, tz, 0))
        self.assertEqual(sd8.sunset .tuple(),     (2033, 10, 22,  0, 12, 0, 0, tz, 0))
        self.assertTrue (sd8.is_daytime  (datetime(2033, 10, 21, 12,  6, 0, 0, tz)))
        self.assertFalse(sd8.is_nighttime(datetime(2033, 10, 21, 23, 59, 0, 0, tz)))
        self.assertTrue (sd8.is_sunrise  (datetime(2033, 10, 21,  3,  6, 0, 0, tz)))
        self.assertTrue (sd8.is_sunset   (datetime(2033, 10, 22,  0, 12, 0, 0, tz)))

if __name__ == '__main__':
        unittest.main()
