# Sunrise and Sunset Time

This library provides an approximated calculation of sunrise and sunset time.
It is written in Python and targets the [MicroPython](http://micropython.org)'s
constrained environments.

More specifically, given a `date` and the coordinate pair `(latitude,
longitude)` of a place on Earth, this library computes when sun rises above di
horizon and when it sets down on that day in that place. Methods are provided
for checking whether current time is daytime, nighttime, sunrise or sunset
time.


## Implementations

The library consists of two implementations: classes `Sundatetime` and
`Suntime`. They differ from the input and output data types. The former makes
use of standard library's `datetime`: it's easier to use but requires more RAM.
If target board resources are constrained, the latter offers a viable solution
by working with integers.


### Class `Sundatetime`

This class makes use of module `datetime` for expressing input date and output
time. The following methods are available to the user:

* `Sundatetime(latitude, longitude, altitude=0)`
  
  Arguments *latitude* and *longitude* are floats representing the coordinates
  of a place on Earth. *altitude* is an integer number for observer's elevation
  in meters.
  
* `Sundatetime.calc_sunrise_sunset(date)`
  
  Calculate the sunrise and sunset for the given date. *date* must be an
  *aware* `datetime.datetime` object in the range [2000-01-01; 2100-01-01).
  Time information is ignored, whereas time zone `tzinfo` is used to provide
  meaningful output. The results are cached in `sunrise` and `sunset` instance
  variables.
  
* `Sundatetime.is_daytime(now)` and `Sundatetime.is_nighttime(now)`
  
  Argument *now* is an *aware* `datetime.datetime` object representing a point
  in time. A boolean value is returned whether Sun is above/below the horizon
  or not, `None` when data are meaningless.
  
* `Sundatetime.is_sunrise(now)` and `Sundatetime.is_sunset(now)`
  
  Argument *now* is an *aware* `datetime.datetime` object representing a point
  in time. A boolean value is returned whether *now* matches sunrise/sunset
  time or not, `None` when data are meaningless.


The following instance variables are accessible:

* `Sundatetime.latitude` and `Sundatetime.longitude`
  
  Float numbers for coordinates on Earth.
  
* `Sundatetime.altitude`
  
  Elevation in meters for observations above the sea horizon. It corrects for
  both apparent dip and terrestrial refraction.
  
* `Sundatetime.sunrise` and `Sundatetime.sunset`
  
  They hold `None` when an instance is created, an *aware* `datetime.datetime`
  after `calc_sunrise_sunset()` is called.

> [!NOTE]
> `Sundatetime.sunrise` may occur before 00:00 and `Sundatetime.sunset` after
> 23:59 on calculated *date*. See [Unexpected results](#unexpected-results).



### Class `Suntime`

The following class makes use of plain integers for expressing input date and
output time. The following methods are available to the user:

* `Suntime(latitude, longitude, altitude=0, timezone=0)`
  
  Arguments *latitude* and *longitude* are floats representing the
  coordinates of a place on Earth. *altitude* is an integer number for
  observer's elevation in meters. *timezone* is an integer holding the
  timezone offset from UTC in minutes. The results are cached in
  `sunrise` and `sunset` instance variables.
  
* `Suntime.calc_sunrise_sunset(year, month, day, dst=0)`
  
  Calculate the sunrise and sunset for the given year, month and day.
  *year* must be in the range [2000; 2100). *dst* is an integer holding the
  offset in minute (usually 60) that accounts for Daylight Saving Time.
  
* `Suntime.is_daytime(now)` and `Suntime.is_nighttime(now)`
  
  Argument *now* is an integer holding the number of minutes since midnight.
  A boolean value is returned whether Sun is above/below the horizon or not,
  `None` when data are meaningless.
  
* `Suntime.is_sunrise(now)` and `Suntime.is_sunset(now)`
  
  Argument *now* is an an integer holding the number of minutes since midnight.
  A boolean value is returned whether *now* matches sunrise/sunset time or not,
  `None` when data are meaningless.


The following instance variables are accessible:

* `Suntime.latitude`  and `Suntime.longitude`
  
  Float numbers for coordinates on Earth.
  
* `Suntime.altitude`
  
  Elevation in meters for observations above the sea horizon. It corrects
  for both apparent dip and terrestrial refraction.
  
`Suntime.sunrise` and `Suntime.sunset`
  
  It holds `None` when an instance is created, an integer for the
  difference in minutes since 00:00 after `calc_sunrise_sunset()`
  is called.

> [!NOTE]
> `Suntime.sunrise` may be negative and `Suntime.sunset` may be greater than
> 1439 (24 hours). See [Unexpected results](#unexpected-results).


### Unexpected results

Class `Sundatetime` may return unexpected results: `Sundatetime.sunrise` may
come before 00:00 and/or `Sundatetime.sunset` may come after 23:59. Similarly,
class `Suntime` may return a negative `Suntime.sunrise` and/or a
`Suntime.sunset` greater or equal to 1440 (24 hours).

Assuming `date` is the current date and `now` is the current time, the
conditions which may lead to unexpected results are:

* *incorrect time zone*: *date*'s time zone is not consistent with provided
  *longitude*. Suitable values for *timezone* and *dst* should be provided. See
  example at Novosibirsk in [example.py].

* *Sun is up all day*: close to the poles, Sun never sets in summer/winter
  time. For this dates, `is_daytime()` holds true for the whole `date`. Note
  that the following holds true: `sunrise ≤ now < sunset`.

* *Sun is down all day*: close to the poles, Sun never raises in summer/winter
  time. For this dates, `is_nighttime()` holds true for the whole `date`.
  Note that the following holds false: `sunrise < sunset`.

* *Sun sets after midnight*: close to the poles, Sun may sets after 23:59. In
  this case, `is_daytime()` and `is_nighttime()` behave as expected. The
  following condition is true: `sunrise ≤ now ≤ 23:59 < sunset`.


## Installation

You can simply copy the content of directory `suntime`. If only one
implementation is needed, the other can be deleted.

Alternatively, MicroPython's tool `mip` can be exploited to install one
implementation or the whole library. As reference, choose one of the following
commands for installing the library on your Unix port:

```sh
micropython -m mip install github:lorcap/micropython-suntime/sundatetime-package.json
micropython -m mip install github:lorcap/micropython-suntime/suntime-package.json
micropython -m mip install github:lorcap/micropython-suntime
```

See MicroPython's [Package management](https://docs.micropython.org/en/latest/reference/packages.html)
for further details.


## Examples of usage

### Typical use case

A typical use case for an embedded system is:

```py
import datetime, time
from suntime.sundatetime import Sundatetime

class Cet(datetime.timezone):
    # See `datetime` documentation

# initialization
CET = Cet()
Rome = Sundatetime(42.5966460, 12.4360233)
Rome.calc_sunrise_sunset(datetime.datetime(2000, 1, 1, tzinfo=CET))

# main loop (every minute or more)
now = datetime.datetime(*time.localtime()[:5], tzinfo=CET)
if (now.date() > Rome.sunset.date()):
    Rome.calc_sunrise_sunset(now)
Rome.is_daytime(now)
```

### Sunrise and sunset around the globe

The script provided in [example.py] shows sunrise and sunset time for several
places and dates.


[REFERENCES]: #

[example.py]: example.py "Script with examples"
