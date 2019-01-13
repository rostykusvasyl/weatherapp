""" Abstract classes for project.
"""

import abc
import time
import hashlib
import argparse
import configparser
from pathlib import Path
import requests

import config


class Command(abc.ABC):
    """ Base class for commands.

    :param app: Main application instance
    :type app: app.App
    """

    def __init__(self, app):
        self.app = app

    @staticmethod
    def get_parser():
        """ Initialize argument parser for command.
        """

        parser = argparse.ArgumentParser()
        return parser

    @abc.abstractmethod
    def run(self, argv):
        """ Invoked by application when the command is run.

        Should be overriden in subclass.
        """


class WeatherProvider(Command):
    """ Weather provider abstract class.

    """

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
    def _get_configuration_file():
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
            configuration.read(self._get_configuration_file())
        except configparser.Error:
            print(f"Bad configuration file. "
                  f"Please reconfigurate your provider: {self.get_name()}")
            if self.app.options.debug:
                raise
        if config.CONFIG_LOCATION in configuration.sections():
            locatoin_config = configuration[config.CONFIG_LOCATION]
            name, url = locatoin_config['name'], locatoin_config['url']
        return name, url

    def save_configuration(self, name, url):
        """ Write the data received from the user (the city name and its URL)
        into the configuration file.
        """

        parser = configparser.ConfigParser()
        config_file = self._get_configuration_file()

        if config_file.exists():
            try:
                parser.read(config_file)
            except configparser.Error:
                print(f"Bad configuration file. "
                      f"Please reconfigurate your provider: {self.get_name()}")
                if self.app.options.debug:
                    raise

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
            page = requests.get(url, headers=headers)
            page = page.content
            self.save_cache(url, page)
        return page.decode('utf-8')

    def run(self, argv):
        """ Run provider.
        """

        content = self.get_page_source(self.url)
        return self.get_weather_info(content)


class Manager(abc.ABC):
    """ Abstract class for project command managers
    """

    @abc.abstractmethod
    def add(self, name, command):
        """ Add new command to manager.

        :param name: command name
        :type name: str
        :param command: command class
        :type command : Sub type of 'weather.abstract.Command'

        """

    @abc.abstractmethod
    def get(self, name):
        """ Get command from manager by name

        :param name: command name
        :type name: str

            """

    @abc.abstractmethod
    def __getitem__(self, name):
        """ Get item by name.

        Implementation of this 'danger' method allow us to access commands
        by name in the same way at it works in dictionary.

        :param name: command name
        :type name: str

        """

    @abc.abstractmethod
    def __contains__(self, name):
        """ Check if command with provider name is in manager.

        Implementation of this 'danger' method allow us to use 'in'
        operator with manager to check if command exists in manager.

        :param name: command name
        :type name: str

        """
