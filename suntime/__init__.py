"""Sunrise and sunset computation"""
__version__ = "1.0.0"

from math import acos, asin, cos, degrees as deg, fmod as mod,\
                 sqrt, radians as rad, sin

# https://en.wikipedia.org/wiki/Sunrise_equation
# https://en.wikipedia.org/wiki/Julian_day
#  m = round((M - 14)/12)
#  JDN = round(1461*(Y + 4800 + m)/4)\
#      + round((367*(M - 2 - 12*m))/12)\
#      - round((3*(round((Y + 4900 + m)/100)))/4)\
#      + D - 32075
def equation (n: int, lat: float, lon: float, alt: float) -> tuple[float, float]:
    #  n = ceil(Jd - 2451545.0 + 0.0008)
    assert(0 <= n < 36525) # days in 21st century
    Js = n - lon/360
    M = mod(357.5291 + 0.98560028*Js, 360)
    C = 1.9148*sin(rad(M)) + 0.0200*sin(rad(2*M)) + 0.0003*sin(rad(3*M))
    λ = mod(M + C + 180 + 102.9372, 360)
    Jt = 2451545.0 + Js + 0.0053*sin(rad(M)) - 0.0069*sin(rad(2*λ))
    sinδ = sin(rad(λ))*sin(rad(23.44))
    cosω0 = (sin(rad(-0.83 - 2.076*sqrt(alt)/60)) - sin(rad(lat))*sinδ)\
          / (cos(rad(lat))*cos(asin(sinδ)))
    if cosω0 <= -1.0:
        ω0 = 360
    elif cosω0 >= 1.0:
        ω0 = -360
    else:
        ω0 = deg(acos(cosω0))
    Jr = Jt - ω0/360
    Js = Jt + ω0/360
    return Jr, Js

def jdate2time (Jd: float, n: int, tz: int=0) -> int:
    jtime = Jd - (2451545 + n)
    minutes = round(jtime*1440) + 720 + tz
    return minutes
