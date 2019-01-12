""" Main application module.
"""


import sys
import argparse
from abstract import WeatherProvider, Providers
from providermanager import ProviderManager


class App:
    """ Weather aggregator application.
    """

    def __init__(self):
        self.arg_parser = self._arg_parser()
        self.providermanager = ProviderManager()

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
            '--refresh', help='Update cache', action='store_true'
            )
        arg_parser.add_argument(
            '--debug', help='Shows all the error information',
            action='store_true'
            )
        arg_parser.add_argument(
            '--clear_cache', help='Remove cache directory', action='store_true'
            )
        arg_parser.add_argument(
            '--config', help='Create configuration file', action='store_true'
            )
        arg_parser.add_argument('--provider', help='Command displays all\
                                existing providers.', action='store_true')
        return arg_parser

    @staticmethod
    def output(title, location, info):
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

        if not command_name:
            # run all weather providers by default
            try:
                if self.options.clear_cache:
                    WeatherProvider.remove_cache()
                elif self.options.provider:
                    Providers.run(self, argv)
                else:
                    for provider in self.providermanager._providers.values():
                        provider_obj = provider(self)
                        self.output(provider_obj.title, provider_obj.location,
                                    provider_obj.run(remaining_args))
            except Exception:
                print('----------------------------------'
                      '----------------------------------------')
                print("The program ended up crashing. Contact developers for "
                      "more information.!!!")
                print('----------------------------------'
                      '----------------------------------------')
                if self.options.debug:
                    raise

        if command_name in self.providermanager:
            # run specific provider
            try:
                provider = self.providermanager[command_name]
                provider_obj = provider(self)
                if self.options.clear_cache:
                    provider_obj.remove_cache()
                if self.options.config:
                    provider_obj.configurate()
                else:
                    self.output(provider_obj.title, provider_obj.location,
                                provider_obj.run(remaining_args))
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
