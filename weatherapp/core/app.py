""" Main application module.
"""

import sys
import logging
from argparse import ArgumentParser
from weatherapp.core import config
from weatherapp.core.formattermanager import FormatterManager
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
        self.formattermanager = FormatterManager()

    @staticmethod
    def _arg_parser():
        """ Initialize argument parser.
        """

        arg_parser = ArgumentParser(description='A simple program for '
                                    'displaying weather information.')
        arg_parser.add_argument('command', help='Use commands: "accu" - for'
                                'the Accuwether website or "rp5" - for'
                                'the Rp5 site or "sinoptik" - for '
                                'the sinoptik.ua, "configurate" - to determine'
                                ' location, "clear_cache" - for remove cache.',
                                nargs='?')
        arg_parser.add_argument(
            '--refresh', help='Update cache.', action='store_true')
        arg_parser.add_argument(
            '--debug', help='Shows all the error information.',
            action='store_true')
        arg_parser.add_argument(
            'tomorrow', help='Show weather information for the next day.',
            nargs='?')
        arg_parser.add_argument(
            '--align', help='Change the alignment of all the columns. '
            'The allowed strings are "l", "r" and "c" for left, right and '
            'centre alignment, defaults to left alignment.',
            default='l', nargs='?')
        arg_parser.add_argument(
            '-p_w', '--padding_width', help='Number of spaces on either '
            'side of column data. Defaults is 1.',
            default=1, nargs='?')
        arg_parser.add_argument(
            '-v_char', '--vertical_char', help='Single character string '
            'used to draw vertical lines. Default is "|".',
            nargs='?')
        arg_parser.add_argument(
            '-h_char', '--horizontal_char', help='Single character string '
            'used to draw horizontal lines. Default is "-".',
            nargs='?')
        arg_parser.add_argument(
            '--set_style', help='Setting a table style: '
            '"DEFAULT" - the default look. '
            '"PLAIN_COLUMNS" - a borderless style. '
            '"MSWORD_FRIENDLY" - print a table in a format Microsoft Word’s.',
            default='DEFAULT', nargs='?')
        arg_parser.add_argument(
            '-v', '--verbose', action='count',
            dest='verbose_level', default=config.DEFAULT_VERBOSE_LEVEL,
            help='Increase verbosity of output.')
        arg_parser.add_argument(
            '-f', '--formatter', default='table',
            nargs='?', help="Output format, defaults to table.")

        return arg_parser

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

        formatter_name = self.options.formatter
        if formatter_name:
            formatter = self.formattermanager.get(formatter_name)
            self.stdout.write('{}: \n'.format(title))
            if not self.options.tomorrow:
                columns = [location, 'today']
            else:
                columns = [location, 'tomorrow']
            formatter().emit(columns, data)
            self.stdout.write('\n')
        else:
            self.stdout.write('{}:\n'.format(title))
            self.stdout.write('*' * 12)
            self.stdout.write('\n')
            if not self.options.tomorrow:
                self.stdout.write('{} {}\n'.format(location, 'today'))
            else:
                self.stdout.write('{} {}\n'.format(location, 'tomorrow'))
            self.stdout.write("_" * 20)
            self.stdout.write('\n')
            for key, value, in data.items():
                self.stdout.write('{0}: {1} \n'.format(key, value))
            self.stdout.write("=" * 40)
            self.stdout.write('\n\n')

    def run_command(self, name, argv):
        """ Run command
        """
        command = self.commandmanager.get(name)
        try:
            command(self).run(argv)
        except Exception:
            msg = "Error during command: %s run"
            if self.options.debug:
                self.logger.exception(msg, name)
            else:
                self.logger.error(msg, name)

    def run_provider(self, name, argv):
        """ Run specified provider
        """

        provider = self.providermanager.get(name)
        if provider:
            provider = provider(self)
            self.output_weather_info(provider.title,
                                     provider.location,
                                     provider.run(argv))

    def run_providers(self, argv):
        """ Execute all available providers.
        """

        for name, provider in self.providermanager:
            provider = provider(self)
            self.output_weather_info(provider.title,
                                     provider.location,
                                     provider.run(argv))

    def run(self, argv):
        """ Run application.
        :param argv: list of passed arguments
        """

        self.options, remaining_args = self.arg_parser.parse_known_args(argv)
        self.configurate_logging()

        command_name = self.options.command

        if not command_name:
            # run all providers
            return self.run_providers(remaining_args)

        if command_name == 'tomorrow':
            # run all providers and show weather for tomorrow
            self.options.tomorrow = 'tomorrow'
            return self.run_providers(self.options.tomorrow)

        if command_name in self.commandmanager:
            return self.run_command(command_name, remaining_args)

        if command_name in self.providermanager:
            return self.run_provider(command_name, remaining_args)


def main(argv=sys.argv[1:]):
    """ Main entry point.
    """

    try:
        return App().run(argv)
    except KeyboardInterrupt:
        sys.stdout.write(" Oops!!! Someone closed the program.\n")


if __name__ == '__main__':
    main(sys.argv[1:])
