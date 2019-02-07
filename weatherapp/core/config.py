""" Module contains constants (default values).
"""

# application default verbose and log levels
DEFAULT_VERBOSE_LEVEL = 0
DEFAULT_MESSAGE_FORMAT = '%(message)s'

# A file in which the data about the city and the address for which weather
# conditions will be displayed will be recorded.
CONFIG_LOCATION = 'Location'
CONFIG_FILE = 'weatherapp.ini'

# The directory where the cached data will be stored.
CACHE_DIR = 'weather_cache'

# The time at which you want to update the cache.
CACHE_TIME = 300

# entry points group for providers
PROVIDER_EP_NAMESPACE = 'weatherapp.provider'
