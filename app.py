""" Main application module.
"""


import sys
import argparse
from commandmanager import CommandManager
from providermanager import ProviderManager


class App:
    """ Weather aggregator application.
    """

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
            '--refresh', help='Update cache', action='store_true'   )
        arg_parser.add_argument(
            '--debug', help='Shows all the error information',
            action='store_true')

        return arg_parser

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
        command_name = self.options.command

        if command_name in self.commandmanager:
            command_factory = self.commandmanager.get(command_name)
            try:
                command_factory(self).run(remaining_args)
            except Exception:
                print('----------------------------------'
                      '----------------------------------------')
                print("The program ended up crashing. Contact developers for "
                      "more information.!!!")
                print('----------------------------------'
                      '----------------------------------------')
                if self.options.debug:
                    raise

        if not command_name:
            # run all command providers by default

            try:
                for provider in self.providermanager._commands.values():
                    self.output_weather_info(provider(self).title,
                                             provider(self).location,
                                             provider(self).run(remaining_args))
            except Exception:
                print('----------------------------------'
                      '----------------------------------------')
                print("The program ended up crashing. Contact developers for "
                      "more information.!!!")
                print('----------------------------------'
                      '----------------------------------------')
            if self.options.debug:
                raise

        elif command_name in self.providermanager:
            try:
                provider = self.providermanager[command_name](self)
                self.output_weather_info(provider.title,
                                         provider.location,
                                         provider.run(remaining_args))
            except Exception:
                print('----------------------------------'
                      '----------------------------------------')
                print("The program ended up crashing. Contact developers for "
                      "more information.!!!")
                print('----------------------------------'
                      '----------------------------------------')
            if self.options.debug:
                raise


def main(argv):
    """ Main entry point.
    """
    try:
        return App().run(argv)
    except KeyboardInterrupt:
        print(" Oops!!! Something went wrong. Please restart your program.")


if __name__ == '__main__':
    main(sys.argv[1:])
