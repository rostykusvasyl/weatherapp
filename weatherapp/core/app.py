""" Main application module.
"""

import sys
import logging
from argparse import ArgumentParser

from weatherapp.core.formatters import TableFormatter, CsvFormatter
from weatherapp.core import config
from weatherapp.core.commandmanager import CommandManager
from weatherapp.core.providermanager import ProviderManager


class App:
    """ Weather aggregator application.
    """

    logger = logging.getLogger(__name__)
    LOG_LEVEL_MAP = {0: logging.WARNING,
                     1: logging.INFO,
                     2: logging.DEBUG}

    def __init__(self, stdin=None, stdout=None, stderr=None):
        self.stdin = stdin or sys.stdin
        self.stdout = stdout or sys.stdout
        self.stderr = stderr or sys.stderr
        self.arg_parser = self._arg_parser()
        self.providermanager = ProviderManager()
        self.commandmanager = CommandManager()
        self.formatters = self._load_formatters()
        self.options = self.arg_parser.parse_args()

    def _arg_parser(self):
        """ Initialize argument parser.
        """

        arg_parser = ArgumentParser(add_help=False)
        arg_parser.add_argument('command', help='Enter "accu" for the '
                                'Accuwether website or "rp5" for the Rp5'
                                ' site or "sinoptik" for the sinoptik.ua',
                                nargs='?')
        arg_parser.add_argument(
            '--refresh', help='Update cache', action='store_true')
        arg_parser.add_argument(
            '--debug', help='Shows all the error information',
            action='store_true')
        arg_parser.add_argument('clear_cache', help='Remove cache \
                        directory', action='store_true')
        arg_parser.add_argument(
            '-v', '--verbose', action='count',
            dest='verbose_level', default=config.DEFAULT_VERBOSE_LEVEL,
            help='Increase verbosity of output')
        arg_parser.add_argument('-f', '--formatter', nargs='?',
                                help="Output format, defaults to table")
        arg_parser.add_argument('csv_write', help='Writing weather data \
                                in .csv format.', action='store_true')

        return arg_parser

    @staticmethod
    def _load_formatters():
        return {'csvtable': CsvFormatter, 'table': TableFormatter}

    def configurate_logging(self):
        """ Create logging handlers for any log output.
        """

        # create logger
        root_logger = logging.getLogger('')
        root_logger.setLevel(logging.DEBUG)

        # create file write handler and set level to debug
        file_write = logging.FileHandler(filename="weatherapp.log")
        file_write.setLevel(logging.DEBUG)

        # create formatter add formatter to file write
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s'
                                      ' - ' + config.DEFAULT_MESSAGE_FORMAT)
        file_write.setFormatter(formatter)

        # add file write to logger
        root_logger.addHandler(file_write)

        # create console handler and set level to debug
        console = logging.StreamHandler()
        console_level = self.LOG_LEVEL_MAP.get(self.options.verbose_level,
                                               logging.WARNING)
        console.setLevel(console_level)

        # create formatter
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s'
                                      ' - ' + config.DEFAULT_MESSAGE_FORMAT)

        # add formatter to console
        console.setFormatter(formatter)

        # add console to logger
        root_logger.addHandler(console)

    def output_weather_info(self, title, location, data):
        """ Displays the result of the received values the state of
            the weather.
        """

        if self.options.formatter == 'csvtable':
            formatter = \
                self.formatters.get(self.options.formatter, 'csvtable')()
            columns = [title, location]
            formatter.emit(columns, data)
            self.stdout.write('\n')

        elif self.options.formatter == 'table':
            formatter = self.formatters.get(self.options.formatter, 'table')()
            columns = [title, location]
            self.stdout.write(formatter.emit(columns, data))
            self.stdout.write('\n')

        else:
            self.stdout.write('{}:\n'.format(title))
            self.stdout.write('*' * 12)
            self.stdout.write('\n')
            self.stdout.write('{}\n'.format(location))
            self.stdout.write("_" * 20)
            self.stdout.write('\n')
            for key, value, in data.items():
                self.stdout.write('{0}: {1} \n'.format(key, value))
            self.stdout.write("=" * 40)
            self.stdout.write('\n\n')

    def run(self, argv):
        """ Run application.
        :param argv: list of passed arguments
        """

        self.options, remaining_args = self.arg_parser.parse_known_args()
        self.configurate_logging()

        command_name = self.options.command
        if command_name in self.commandmanager:
            command_factory = self.commandmanager.get(command_name)
            try:
                command_factory(self).run(argv)
            except Exception:
                msg = "Error during command: %s run"
                if self.options.debug:
                    self.logger.exception(msg, command_name)
                else:
                    self.logger.error(msg, command_name)

        if not command_name:
            # run all command providers by default

            try:
                for provider in self.providermanager._commands.values():
                    self.output_weather_info(provider(self).title,
                                             provider(self).location,
                                             provider(self).run(remaining_args)
                                             )
            except Exception:
                msg = "Error during command: %s"
                if self.options.debug:
                    self.logger.exception(msg, command_name)
                else:
                    self.logger.error(msg, command_name)

        elif command_name in self.providermanager:
            try:
                provider = self.providermanager[command_name](self)
                self.output_weather_info(provider.title,
                                         provider.location,
                                         provider.run(remaining_args))
            except Exception:
                msg = "Error during command: %s run"
                if self.options.debug:
                    self.logger.exception(msg, command_name)
                else:
                    self.logger.error(msg, command_name)


def main(argv=sys.argv[1:]):
    """ Margv=sys.argv[1:]ain entry point.
    """

    try:
        return App().run(argv)
    except KeyboardInterrupt:
        sys.stdout.write(" Oops!!! Something went wrong."
                         "Please restart your program.")


if __name__ == '__main__':
    main(sys.argv[1:])
