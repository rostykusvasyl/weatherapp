import unittest
import argparse
import logging

from weatherapp.core.app import App
from weatherapp.core.formatters import TableFormatter, CsvFormatter


class AppTestCase(unittest.TestCase):

    """ Test application class methods.
    """

    def setUp(self):
        self.parser = App._arg_parser()

    def test_arg_parser(self):
        """ Test application argument parser creation.
        """

        self.assertIsInstance(self.parser, argparse.ArgumentParser)

    def test_arg_parser_default_values(self):
        """ Test application argument parser default values.
        """

        parsed_args = self.parser.parse_args([])
        self.assertIsNone(parsed_args.command)
        self.assertFalse(parsed_args.debug)
        self.assertIsNone(parsed_args.formatter)

    def test_arg_parser_arg(self):
        """ Test application argument parser.
        """

        parsed_args = self.parser.parse_args(['accu', '--debug', '--refresh',
                                              '-v'])

        self.assertEqual(parsed_args.command, 'accu')
        self.assertTrue(parsed_args.debug)
        self.assertIsNone(parsed_args.formatter)
        self.assertTrue(parsed_args.refresh)
        self.assertEqual(parsed_args.verbose_level, 1)

    def test_loads_formatters(self):
        """ Test application _load_formatters.
        """

        app = App()
        formatter = {'table': TableFormatter, 'csvtable': CsvFormatter}
        self.assertDictEqual(formatter, app._load_formatters())

    def test_logging(self):
        """ Test applications for logging;
        """

        logger = logging.getLogger('')
        self.assertIsInstance(logger, logging.Logger)

        # Checks to see if this logger has any handlers configured.
        # Returns True if a handler was found, else False.
        self.assertTrue(logger.hasHandlers())
