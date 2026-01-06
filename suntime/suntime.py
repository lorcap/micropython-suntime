# suntime.py

from . import equation, jdate2time

def day2000(
    year: int,
    month: int,
    day: int,
) -> int:
    assert(2000 <= year < 2100)
    assert(1 <= month <= 12)
    assert(1 <= day <= 31)
    MONTH_DAYS = (31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30)
    return (year - 2000)*365\
         + sum(MONTH_DAYS[:month - 1])\
         + (year if month >= 3 else year - 1)//4\
         + day\
         - 500 # 500 = 499 (non-leap years before 2000) + 1 (Jan 1st 2000)

class Suntime:
    def __init__(
        self,
        latitude: float,
        longitude: float,
        altitude: int=0,
        timezone: int=0,
    ) -> None:
        self.latitude: float = latitude
        self.longitude: float = longitude
        self.altitude: int = altitude
        self.timezone: int = timezone
        self.sunrise: int|None = None
        self.sunset: int|None = None

    def calc_sunrise_sunset(
        self,
        year: int,
        month: int,
        day: int,
        dst: int=0,
    ) -> None:
        n = day2000(year, month, day)
        Jr, Js = equation(n, self.latitude, self.longitude, self.altitude)
        tz = self.timezone + dst
        self.sunrise = jdate2time(Jr, n, tz)
        self.sunset  = jdate2time(Js, n, tz)

    def is_daytime (
        self,
        minutes: int,
    ) -> bool|None:
        if self.sunrise is None or self.sunset is None:
            return None
        if not 0 <= minutes < 1440:
            return None
        return self.sunrise <= minutes < self.sunset

    def is_nighttime (
        self,
        minutes: int,
    ) -> bool|None:
        daytime = self.is_daytime(minutes)
        if daytime is None:
            return None
        return not daytime

    def is_sunrise (
        self,
        minutes: int,
    ) -> bool|None:
        return self.is_daytime(minutes) and minutes == self.sunrise

    def is_sunset (
        self,
        minutes: int,
    ) -> bool|None:
        return self.is_nighttime(minutes) and minutes == self.sunset
