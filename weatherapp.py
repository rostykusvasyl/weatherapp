#! /usr/bin/env python3

''' Module to run all program functions'''

import argparse

import sys

import csv

from providers import AccuWeatherProvider

from providers import Rp5WeatherProvider


ACCU = AccuWeatherProvider()  # Create an instance of the class
RP5 = Rp5WeatherProvider()  # Create an instance of the class


def remove_cache(clear_cache=False):
    ''' Remove cache directory.
    '''
    ACCU.remove_cache(clear_cache=clear_cache)


def output(city_name, info):
    ''' Displays the result of the received values the state of the weather.
    '''

    print("{}".format(city_name).center(20, '='))
    for key, value in info.items():
        print(key, value)
    print('\n')



def get_accu_weather_info(refresh=False):
    '''Displays the weather data for the specified city from the configuration file to the screen.
    '''

    output(ACCU.location, ACCU.run(refresh=refresh))

def configurate(refresh=False):
    ''' The user chooses the city for which he wants to get the weather.
    '''
    ACCU.configurate(refresh=refresh)


def get_rp5_weather_info(refresh=False):
    '''Displays the weather data for the specified city from the configuration file to the screen.
    '''

    output(RP5.location, RP5.run(refresh=refresh))


def configurate_rp5(refresh=False):
    ''' The user chooses the city for which he wants to get the weather.
    '''

    RP5.configurate_rp5(refresh=refresh)


def writer_file_in_csv(refresh=False):
    '''write data in file format .csv'''

    data = [ACCU.run(), RP5.run()]
    with open('csv_weather.csv', 'wt') as frecord:
        #frecord.write(name + '\n')
        writer = csv.DictWriter(frecord, fieldnames=list(data[0].keys()))
        writer.writeheader()
        writer.writerows(data)


def main(argv):
    '''#Main entry point in program.
    '''
    command_list = {'accu': get_accu_weather_info,
                    'rp5': get_rp5_weather_info,
                    'config': configurate,
                    'config_rp5': configurate_rp5,
                    'csv': writer_file_in_csv}

    parser = argparse.ArgumentParser(prog='PROG_WEATHER',
                                     description='Displaying weather information.')

    parser.add_argument('--version', action='version', version='%(prog)s 0.0.1')
    parser.add_argument('command', help='Enter "accu" for the '
                        'Accuwether website or "rp5" for the '
                        'Rp5 site.', nargs='*')
    parser.add_argument('--refresh', help='Update cache', action='store_true')
    parser.add_argument('--clear_cache', help='Remove cache directory',
                        action='store_true')
    args = parser.parse_args(argv)

    LIST_PROVIDERS = [ACCU, RP5]

    if args.command:
        command = args.command[0]
        if command in command_list:
            command_list[command](refresh=args.refresh)
        else:
            print('Unknown command provided!')
            sys.exit(1)
    elif args.clear_cache:
        remove_cache(clear_cache=args.clear_cache)
    else:
    #     output('Accuwether', get_accu_info(refresh=args.refresh))
    #     output('Rp5', get_rp5_info(refresh=args.refresh))
        for provider in LIST_PROVIDERS:
            output(provider.location, provider.run(refresh=args.refresh))



if __name__ == "__main__":
    main(sys.argv[1:])
