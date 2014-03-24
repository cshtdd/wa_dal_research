# development
# > brew install redis
# > sudo pip install redis
# > redis-server

# deployment
# > sudo apt-get install redis-server
# > sudo pip install redis

from datetime import datetime
from datetime import timedelta
import redis

def main():
    days_count = 3
    hours_count = 24
    latitudes_count = 800
    longitudes_count = 50
    total = days_count * hours_count * longitudes_count * latitudes_count
    current = 0

    expiration = days_count * hours_count * 60 * 60
    rdb = redis.StrictRedis()
    rpipe = rdb.pipeline()

    for day in _get_days(days_count):
        for hour in _get_hours(hours_count):
            for latitude in _get_coordinate_component(longitudes_count):
                for longitude in _get_coordinate_component(latitudes_count):
                    key_str = _get_key(day, hour, latitude, longitude)
                    rpipe.hmset(key_str, _get_value()).expire(key_str, expiration).execute()

                current += latitudes_count
                percent = current * 100.0 / total
                print percent, "% ", key_str

def _get_value():
    return {
        "liquid_precipitation_inches": _get_liquid_precipitation_inches(),
        "pop12_percent": _get_pop12_percent(),
        "snow_inches": _get_snow_inches(),
        "apparent_temperature_f": _get_apparent_temperature()
    }

def _get_key(date, hour, latitude, longitude):
    return "location_data:" + "{0}|{1}|{2}|{3}".format(
            date, hour, latitude, longitude
        )

def _get_liquid_precipitation_inches():
    return 0.0

def _get_pop12_percent():
    return 21.0

def _get_snow_inches():
    return 0.0

def _get_apparent_temperature():
    return 55.0

def _get_coordinate_component(max_count):
    for i in range(0, max_count):
        yield "{0:.2f}".format(i / 100.0)

def _get_days(max_days):
    for day_inc in xrange(-max_days, 0):        
        adjusted_date = datetime.utcnow() + timedelta(days=day_inc)
        yield adjusted_date.strftime("%m-%d-%Y")

def _get_hours(max_hour):
    for hour in xrange(0, max_hour):
        yield hour

if __name__ == "__main__":
    main()
