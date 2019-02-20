""" Module container for formatters.
"""


import logging

from weatherapp.core import commandmanager
from weatherapp.core.formatters import CsvFormatter, TableFormatter


class FormatterManager(commandmanager.CommandManager):
    """ Discovers registered formatters and loads them.
    """

    logger = logging.getLogger(__name__)

    def _load_commands(self):
        """ Loads all existing formatters.
        """

        for formatter in [TableFormatter, CsvFormatter]:
            self.add(formatter.name, formatter)
