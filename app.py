""" Main application module.
"""

import logging
import sys
import argparse
from commandmanager import CommandManager
from providermanager import ProviderManager
import config


class App:
    """ Weather aggregator application.
    """

    logger = logging.getLogger(__name__)
    LOG_LEVEL_MAP = {0: logging.WARNING,
                     1: logging.INFO,
                     2: logging.DEBUG}

    def __init__(self):
        self.arg_parser = self._arg_parser()
        self.providermanager = ProviderManager()
        self.commandmanager = CommandManager()

    @staticmethod
    def _arg_parser():
        """
        """

        arg_parser = argparse.ArgumentParser()
        arg_parser.add_argument('command', help='Enter "accu" for the '
                                'Accuwether website or "rp5" for the Rp5'
                                ' site or "sinoptik" for the sinoptik.ua',
                                nargs='?')
        arg_parser.add_argument(
            '--refresh', help='Update cache', action='store_true')
        arg_parser.add_argument(
            '--debug', help='Shows all the error information',
            action='store_true')
        arg_parser.add_argument(
            '-v', '--verbose', action='count',
            dest='verbose_level', default=config.DEFAULT_VERBOSE_LEVEL,
            help='Increase verbosity of output')

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

    @staticmethod
    def output_weather_info(title, location, info):
        """ Displays the result of the received values the state of
            the weather.
        """

        print('{}:'.format(title))
        print("#" * 10, end='\n\n')

        print('{}'.format(location))
        print("_" * 20)
        for key, value, in info.items():
            print('{0:12s} {1}'.format(key, value))
        print("=" * 40, end='\n\n')

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
                command_factory(self).run(remaining_args)
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
                                             provider(self).run(remaining_args))
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

def main(argv):
    """ Main entry point.
    """

    try:
        return App().run(argv)
    except KeyboardInterrupt:
        print(" Oops!!! Something went wrong. Please restart your program.")


if __name__ == '__main__':
    main(sys.argv[1:])
