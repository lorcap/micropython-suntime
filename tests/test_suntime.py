# test_suntime.py

import unittest
from tests import *

from suntime.suntime import Suntime


class TestSunTime(unittest.TestCase):

    def test_suntime1(self):
        st1 = Suntime(*pl1, timezone=tz1[0]*60)
        st1.calc_sunrise_sunset(*dt1, dst=tz1[1]*60)
        assert st1.sunrise is not None # make pyright happy
        assert st1.sunset is not None # make pyright happy
        self.assertEqual(divmod(st1.sunrise, 60), ( 7, 40))
        self.assertEqual(divmod(st1.sunset , 60), (16, 47))
        self.assertFalse(st1.is_daytime( 0*60 +  0))
        self.assertTrue (st1.is_daytime(12*60 +  0))
        self.assertTrue (st1.is_sunrise( 7*60 + 40))
        self.assertTrue (st1.is_sunset (16*60 + 47))
        self.assertIsNone(st1.is_daytime  (  -1))
        self.assertIsNone(st1.is_daytime  (1440))
        self.assertIsNone(st1.is_nighttime(  -1))
        self.assertIsNone(st1.is_nighttime(1440))

    def test_suntime2(self):
        st2 = Suntime(*pl2, timezone=tz2[0]*60)
        st2.calc_sunrise_sunset(*dt2, dst=tz2[1]*60)
        assert st2.sunrise is not None # make pyright happy
        assert st2.sunset is not None # make pyright happy
        self.assertEqual(divmod(st2.sunrise, 60), ( 7, 16))
        self.assertEqual(divmod(st2.sunset , 60), (18, 46))
        self.assertFalse(st2.is_daytime( 0*60 +  0))
        self.assertTrue (st2.is_daytime(12*60 +  0))
        self.assertTrue (st2.is_sunrise( 7*60 + 16))
        self.assertTrue (st2.is_sunset (18*60 + 46))

    def test_suntime3(self):
        st3 = Suntime(*pl3, timezone=tz3[0]*60)
        st3.calc_sunrise_sunset(*dt3, dst=tz3[1]*60)
        assert st3.sunrise is not None # make pyright happy
        assert st3.sunset is not None # make pyright happy
        self.assertEqual(divmod(st3.sunrise, 60), ( 5, 32))
        self.assertEqual(divmod(st3.sunset , 60), (19, 57))
        self.assertFalse(st3.is_daytime( 0*60 +  0))
        self.assertTrue (st3.is_daytime(12*60 +  0))
        self.assertTrue (st3.is_sunrise( 5*60 + 32))
        self.assertTrue (st3.is_sunset (19*60 + 57))

    def test_suntime4(self):
        st4 = Suntime(*pl4, timezone=tz4[0]*60)
        st4.calc_sunrise_sunset(*dt4, dst=tz4[1]*60)
        assert st4.sunrise is not None # make pyright happy
        assert st4.sunset is not None # make pyright happy
        self.assertEqual(divmod(st4.sunrise, 60), (-1,  4))
        self.assertEqual(divmod(st4.sunset , 60), (13, 49))

    def test_suntime5(self):
        st5 = Suntime(*pl5, timezone=tz5[0]*60)
        st5.calc_sunrise_sunset(*dt5, dst=tz5[1]*60)
        assert st5.sunrise is not None # make pyright happy
        assert st5.sunset is not None # make pyright happy
        self.assertEqual(divmod(st5.sunrise, 60), (-12, 57))
        self.assertEqual(divmod(st5.sunset , 60), ( 36, 57))
        self.assertTrue (st5.is_daytime  (  0*60 +  0))
        self.assertFalse(st5.is_nighttime( 12*60 +  0))
        self.assertFalse(st5.is_sunrise  (-12*60 + 57))
        self.assertFalse(st5.is_sunset   ( 36*60 + 57))

    def test_suntime6(self):
        st6 = Suntime(*pl6, timezone=tz6[0]*60)
        st6.calc_sunrise_sunset(*dt6, dst=tz6[1]*60)
        assert st6.sunrise is not None # make pyright happy
        assert st6.sunset is not None # make pyright happy
        self.assertEqual(divmod(st6.sunrise, 60), ( 1, 35))
        self.assertEqual(divmod(st6.sunset , 60), (24, 18))
        self.assertTrue (st6.is_sunrise( 1*60 + 35))
        self.assertFalse(st6.is_sunset (24*60 + 18))

    def test_suntime7(self):
        st7 = Suntime(*pl7, timezone=tz7[0]*60)
        st7.calc_sunrise_sunset(*dt7, dst=tz7[1]*60)
        assert st7.sunrise is not None # make pyright happy
        assert st7.sunset is not None # make pyright happy
        self.assertEqual(divmod(st7.sunrise, 60), ( 37, 0))
        self.assertEqual(divmod(st7.sunset , 60), (-11, 0))
        self.assertFalse(st7.is_daytime  ( 12*60 + 0))
        self.assertTrue (st7.is_nighttime( 12*60 + 0))
        self.assertFalse(st7.is_sunrise  ( 37*60 + 0))
        self.assertFalse(st7.is_sunset   (-11*60 + 0))

    def test_suntime8(self):
        st8 = Suntime(*pl8, timezone=tz8[0]*60)
        st8.calc_sunrise_sunset(*dt8, dst=tz8[1]*60)
        assert st8.sunrise is not None # make pyright happy
        assert st8.sunset is not None # make pyright happy
        self.assertEqual(divmod(st8.sunrise, 60), ( 3,  6))
        self.assertEqual(divmod(st8.sunset , 60), (24, 12))
        self.assertTrue (st8.is_daytime  (12*60 +  6))
        self.assertFalse(st8.is_nighttime(23*60 + 59))
        self.assertTrue (st8.is_sunrise  ( 3*60 +  6))
        self.assertFalse(st8.is_sunset   (24*60 + 12))

if __name__ == '__main__':
        unittest.main()
