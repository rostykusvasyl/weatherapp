""" Module contains constants (default values).
"""

# AccuWeather provider reloaded configuration.
ACCU_PROVIDER_NAME = 'accu'
ACCU_PRVIDER_TITLE = 'AccuWeather'

# The name of the city and the address for which we will display the weather
# conditions by default for site accuweather.
DEFAULT_ACCU_LOCATION_NAME = 'Brody'
DEFAULT_ACCU_LOCATION_URL = ('https://www.accuweather.com/uk/ua/'
                             'brody/324506/weather-forecast/324506')

# Address for finding a place for which we will display weather conditions.
ACCU_BROWSE_LOCATIONS = 'https://www.accuweather.com/uk/browse-locations'

# A file in which the data about the city and the address for which weather
# conditions will be displayed will be recorded.
CONFIG_LOCATION = 'Location'
CONFIG_FILE = 'weatherapp.ini'

# The directory where the cached data will be stored.
CACHE_DIR = 'weather_cache'

# The time at which you want to update the cache.
CACHE_TIME = 300


RP5_PROVIDER_NAME = 'rp5'
RP5_PROVIDER_TITLE = 'rp5.ua'

# The name of the city and the address for which we will display the weather
# conditions by default for site rp5.
DEFAULT_RP5_LOCATION_NAME = 'Brody'
DEFAULT_RP5_LOCATION_URL = ('http://rp5.ua/%D0%9F%D0%BE%D0%B3%D0%BE%D0%B'
                            '4%D0%B0_%D0%B2_%D0%91%D1%80%D0%BE%D0%B4%D0%B'
                            '0%D1%85,_%D0%9B%D1%8C%D0%B2%D1%96%D0%B2%D1%81%'
                            'D1%8C%D0%BA%D0%B0_%D0%BE%D0%B1%D0%BB%D0%B0%D1%'
                            '81%D1%82%D1%8C')

# Address for finding a place for which we will display weather conditions.
RP5_BROWSE_LOCATIONS = ('http://rp5.ua/%D0%9F%D0%BE%D0%B3%D0%BE%D0%B4%D0%B0_'
                        '%D0%B2_%D1%81%D0%B2%D1%96%D1%82%D1%96')

# A file in which the data about the city and the address for which weather
# conditions will be displayed will be recorded.
CONFIG_LOCATION = 'Location'



SINOPTIK_PROVIDER_NAME = 'sinoptik'
SINOPTIK_PROVIDER_TITLE = 'sinoptik.ua'

DEFAULT_SINOPTIK_LOCATION_NAME = 'Brody'
DEFAULT_SINOPTIK_LOCATION_URL = ('https://ua.sinoptik.ua/%D0%BF%D0%BE%D0%B3%D0%BE%D0%B'
                        '4%D0%B0-%D0%B1%D1%80%D0%BE%D0%B4%D0%B8')

SINOPTIK_BROWSE_LOCATIONS = ('https://ua.sinoptik.ua/%D1%83%D0%BA%D1%80%D'
                             '0%B0%D1%97%D0%BD%D0%B0')

CONFIG_LOCATION = 'Location'

