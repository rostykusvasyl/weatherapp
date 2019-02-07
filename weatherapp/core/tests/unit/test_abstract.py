import abc
import unittest
from weatherapp.core.abstract import Command
from weatherapp.core.abstract import Formatter
from weatherapp.core.abstract import Manager
from weatherapp.core.abstract import WeatherProvider


class CommandAbsrtact(Command):
    def __init__(self, app):
        self.app = app

    def run(self):
        pass


class FormatterdAbsrtact(Formatter):
    def emit(self):
        pass


class ManagerAbsrtact(Manager):
    def add(self):
        pass

    def get(self):
        pass

    def __getitem__(self, name):
        pass

    def __contains__(self, name):
        pass


class WeatherProviderAbsrtact(Command):
    def __init__(self, app):
        self.app = app

    def get_name(self):
        pass

    def get_default_location(self):
        pass

    def _get_default_url(self):
        pass

    def configurate(self):
        pass

    def get_weather_info(self):
        pass

    def run(self):
        pass


class AbstractTestCase(unittest.TestCase):
    """ Unit test case for abstract classes.
    """
    def test_abstract_command(self):
        """ Test application for abstract class Command.
        """
        self.assertIsInstance(CommandAbsrtact(self), Command)

    def test_abstract_formatter(self):
        """ Test application for abstract class Formatter.
        """
        self.assertIsInstance(FormatterdAbsrtact(), Formatter)

    def test_abstract_manager(self):
        """ Test application for abstract class Manager.
        """
        self.assertIsInstance(ManagerAbsrtact(), Manager)

    def test_containsabstract_provider(self):
        """ Test application for abstract class WeatherProvider.
        """
        self.assertIsInstance(WeatherProviderAbsrtact(self), Command)
