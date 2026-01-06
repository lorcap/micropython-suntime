# sundatetime.py

import datetime
from . import equation, jdate2time

def jdate2datetime(
    Jd: float,
    date: datetime.datetime,
) -> datetime.datetime:
    days = date.toordinal()
    n = days - datetime.datetime(2000, 1, 1).toordinal()
    minutes = jdate2time(Jd, n)
    days_, minutes = divmod(minutes, 1440)
    days += days_
    dt = datetime.datetime(
        0, 0, days,
        microsecond=minutes*60_000_000,
        tzinfo=datetime.timezone.utc)
    if date.tzinfo:
        dt = dt.astimezone(date.tzinfo)
    return dt

class Sundatetime:
    def __init__(
        self,
        latitude: float,
        longitude: float,
        altitude: int=0,
    ) -> None:
        self.latitude: float = latitude
        self.longitude: float = longitude
        self.altitude: int = altitude
        self.sunrise: datetime.datetime|None = None
        self.sunset: datetime.datetime|None = None

    def calc_sunrise_sunset(
        self,
        date: datetime.datetime,
    ) -> None:
        n = date.toordinal() - datetime.datetime(2000, 1, 1).toordinal()
        Jr, Js = equation(n, self.latitude, self.longitude, self.altitude)
        self.sunrise = jdate2datetime(Jr, date)
        self.sunset  = jdate2datetime(Js, date)

    def is_daytime (
        self,
        now: datetime.datetime,
    ) -> bool|None:
        if self.sunrise is None or self.sunset is None:
            return None
        if self.sunrise >= self.sunset:
            return None
        return self.sunrise <= now < self.sunset

    def is_nighttime (
        self,
        now: datetime.datetime,
    ) -> bool|None:
        daytime = self.is_daytime(now)
        if daytime is None:
            return None
        return not daytime

    def is_sunrise (
        self,
        now: datetime.datetime,
    ) -> bool|None:
        return self.is_daytime(now) and self.sunrise == now

    def is_sunset (
        self,
        now: datetime.datetime,
    ) -> bool|None:
        return self.is_nighttime(now) and self.sunset == now
