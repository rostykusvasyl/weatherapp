''' Main application module.
'''


import sys

from argparse import ArgumentParser

from providermanager import ProviderManager


class App(object):
    ''' Weather aggregator application.
    '''

    def __init__(self):
        self.arg_parser = self._arg_parse()
        self.providermanager = ProviderManager()
        self.options, remaining_args = self.arg_parser.parse_known_args()

    def _arg_parse(self):
        ''' Initializate argument parser.
        '''

        arg_parser = ArgumentParser(add_help=True)
        arg_parser.add_argument('command', help='Enter "accu" for the '
                                'Accuwether website or "rp5" for the Rp5'
                                ' site or "sinoptik" for the sinoptik.ua ',\
                                nargs='?')
        arg_parser.add_argument('--refresh', help='Update cache', \
                                action='store_true')
        arg_parser.add_argument('--clear_cache', help='Remove cache \
                                directory', action='store_true')
        arg_parser.add_argument('config', help='Create configuration file', \
                                nargs='?')
        return arg_parser

    def output(self, title, location, info):
        ''' Displays the result of the received values the state of
            the weather.
        '''

        print('{}:'.format(title))
        print("#" * 10, end='\n\n')

        print('{}'.format(location))
        print("_" * 20)
        for key, value, in info.items():
            print('{0:12s} {1}'.format(key, value))
        print("=" * 40, end='\n\n')

    def run(self, argv):
        ''' Run application.
        '''

        command_name = self.options.command

        
        if not command_name:
            # run all weather providers by default

            if not self.options.clear_cache:
                for provider in self.providermanager._providers.values():
                    provider_obj = provider(self)
                    self.output(provider_obj.title, provider_obj.location,\
                                provider_obj.run())
            elif self.options.clear_cache:
                 for provider in self.providermanager._providers.values():
                    provider_obj = provider(self)
                    provider_obj.remove_cache()


        if command_name in self.providermanager:
            # run specific provider

            provider = self.providermanager[command_name]
            provider_obj = provider(self)
            if self.options.clear_cache:
                provider_obj.remove_cache()
            elif self.options.config:
                provider_obj.configurate()
            else:
                self.output(provider_obj.title, provider_obj.location,\
                            provider_obj.run())


def main(argv=sys.argv[1:]):
    ''' Main entry point.
    '''

    return App().run(argv)


if __name__ == '__main__':
    main(sys.argv[1:])
