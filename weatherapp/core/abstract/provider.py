import abc
import time
import hashlib
import logging
import configparser
from pathlib import Path

import requests

from weatherapp.core import config
from weatherapp.core.abstract.command import Command


class WeatherProvider(Command):
    """ Weather provider abstract class.
    """

    # create logger
    logger = logging.getLogger(__name__)

    def __init__(self, app):
        super().__init__(app)

        location, url = self._get_configuration()
        self.location = location
        self.url = url

    @abc.abstractmethod
    def get_name(self):
        """ Get name provider
        """

    @abc.abstractmethod
    def get_default_location(self):
        """ Default location name.
        """

    @abc.abstractmethod
    def get_default_url(self):
        """ Default location url.
        """

    @abc.abstractmethod
    def configurate(self):
        """ Performs provider configuration.
        """

    @abc.abstractmethod
    def _get_configuration(self):
        """ The function returns data from the configuration file,
            if the file is configured, or accepts default data.
        """

    @abc.abstractmethod
    def get_weather_info(self, page):
        """ Collects weather information.
        Gets weather information from source and produce it in the following
        format.

        weather_info = {
            'cond':      ''    # weather condition
            'temp':      ''    # temperature
            'feels_like' ''    # feels like temperature
            'wind'       ''    # information about wind
        }
        """

    @staticmethod
    def get_configuration_file():
        """ The function returns the path to the configuration file.
        """

        return Path.home() / config.CONFIG_FILE

    def _get_configuration(self):
        """ The function returns data from the configuration file,
        if the file is configured, or accepts default data.
        """

        name = self.get_default_location()
        url = self.get_default_url()

        configuration = configparser.ConfigParser()
        try:
            configuration.read(self.get_configuration_file())
        except configparser.Error:
            msg = ("Bad configuration file. "
                   "Please reconfigurate your provider: %s ")
            if self.app.options.debug:
                self.logger.exception(msg, self.get_name())
            else:
                self.logger.error(msg, self.get_name())

        if self.get_name() in configuration.sections():
            locatoin_config = configuration[self.get_name()]
            name, url = locatoin_config['name'], locatoin_config['url']
        return name, url

    def save_configuration(self, name, url):
        """ Write the data received from the user (the city name and its URL)
        into the configuration file.
        """

        parser = configparser.ConfigParser()
        config_file = self.get_configuration_file()

        if config_file.exists():
            parser.read(config_file)

        parser[self.get_name()] = {'name': name, 'url': url}
        with open(config_file, 'w') as configfile:
            parser.write(configfile)

    @staticmethod
    def get_cache_directory():
        """ The function returns the path to the cache directory.
        """

        return Path.home() / config.CACHE_DIR

    @staticmethod
    def get_url_hash(url):
        """ Generates hash for given url.
        """

        return hashlib.md5(url.encode('utf-8')).hexdigest()

    def save_cache(self, url, page):
        """ Save page source by given url address.
        """

        url_hash = self.get_url_hash(url)
        cache_dir = self.get_cache_directory()
        if not cache_dir.exists():
            cache_dir.mkdir(parents=True)

        with (cache_dir / url_hash).open('wb') as cache_file:
            cache_file.write(page)

    @staticmethod
    def is_valid(path):
        """ Check if current cache file is valid.
        """

        return (time.time() - path.stat().st_mtime) < config.CACHE_TIME

    def get_cache(self, url):
        """ Return cache data if any.
        """

        cache = b''
        url_hash = self.get_url_hash(url)
        cache_dir = self.get_cache_directory()
        if cache_dir.exists():
            cache_path = cache_dir / url_hash
            if cache_path.exists() and self.is_valid(cache_path):
                with cache_path.open('rb') as cache_file:
                    cache = cache_file.read()
        return cache

    def get_page_source(self, url):
        """ Get the html-page at the specified url address.
        """

        cache = self.get_cache(url)
        if cache and not self.app.options.refresh:
            page = cache
        else:
            headers = \
                {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64;)'}
            try:
                page = requests.get(url, headers=headers, timeout=5)
            except requests.ConnectionError as msg:
                self.app.stdout.write("OOPS!! Connection Error. Make sure you"
                                      "are connected to Internet. Technical"
                                      "Details given below. \n")
                if self.app.options.debug:
                    self.logger.exception(msg)
                else:
                    self.logger.error(msg)
            except requests.Timeout as msg:
                self.app.stdout.write("OOPS!! Timeout Error")
                if self.app.options.debug:
                    self.logger.exception(msg)
                else:
                    self.logger.error(msg)
            except requests.RequestException as msg:
                self.app.stdout.write("OOPS!! General Error")
                if self.app.options.debug:
                    self.logger.exception(msg)
                else:
                    self.logger.error(msg)
            page = page.content
            self.save_cache(url, page)
        return page.decode('utf-8')

    def run(self, argv):
        """ Run provider.
        """

        content = self.get_page_source(self.url)
        return self.get_weather_info(content)
