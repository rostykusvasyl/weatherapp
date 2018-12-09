#! /usr/bin/env python3

'''Program for web-scraping of weather sites'''

import argparse

import sys

import time

import hashlib

import csv

import configparser

from pathlib import Path

import requests

from bs4 import BeautifulSoup


ACCU_URL = ('https://www.accuweather.com/uk/ua/brody/324506/weather-forecast/324506')
DEFAULT_NAME = 'Brody'
DEFAULT_URL = ('https://www.accuweather.com/uk/ua/brody/324506/current-weather/324506')
ACCU_BROWSE_LOCATIONS = 'https://www.accuweather.com/uk/browse-locations'
CONFIG_LOCATION = 'Location'
CONFIG_FILE = 'weatherapp.ini'
CACHE_DIR = 'weather_cache'
CACHE_TIME = 300

RP5_URL = ('http://rp5.ua/%D0%9F%D0%BE%D0%B3%D0%BE%D0%B4%D0%B0_%D0%'
           'B2_%D0%91%D1%80%D0%BE%D0%B4%D0%B0%D1%85,_%D0%9B%D1%8C%'
           'D0%B2%D1%96%D0%B2%D1%81%D1%8C%D0%BA%D0%'
           'B0_%D0%BE%D0%B1%D0%BB%D0%B0%D1%81%D1%82%D1%8C')
DEFAULT_NAME_RP5 = 'Brody'
DEFAULT_URL_RP5 = ('http://rp5.ua/%D0%9F%D0%BE%D0%B3%D0%BE%D0%B4%D0%B0_%D0%'
                   'B2_%D0%91%D1%80%D0%BE%D0%B4%D0%B0%D1%85,_%D0%9B%D1%8C%'
                   'D0%B2%D1%96%D0%B2%D1%81%D1%8C%D0%BA%D0%'
                   'B0_%D0%BE%D0%B1%D0%BB%D0%B0%D1%81%D1%82%D1%8C')
RP5_BROWSE_LOCATIONS = ('http://rp5.ua/%D0%9F%D0%BE%D0%B3%D0%BE%D0%B4%D0%B0_'
                        '%D0%B2_%D1%81%D0%B2%D1%96%D1%82%D1%96')
CONFIG_LOCATION = 'Location'
CONFIG_FILE_RP5 = 'weather_rp5.ini'


def get_cache_directory():
    '''The function returns the path to the cache directory.
    '''

    return Path.home() / CACHE_DIR


def remove_cache(clear_cache=False):
    ''' Remove cache directory
    '''

    cache_dir = get_cache_directory()
    if cache_dir.exists():
        for current_file in cache_dir.iterdir():
            current_file.unlink()
        cache_dir.rmdir()


def get_url_cache(url):
    ''' Generates has for given url.
    '''

    return hashlib.md5(url.encode('utf-8')).hexdigest()


def save_cache(url, page):
    ''' Save page source by given url address.
    '''

    url_hash = get_url_cache(url)
    cache_dir = get_cache_directory()
    if not cache_dir.exists():
        cache_dir.mkdir(parents=True)

    with (cache_dir / url_hash).open('wb') as cache_file:
        cache_file.write(page)


def is_valid(path):
    '''Check if current cache file is valid.
    '''

    return (time.time() - path.stat().st_mtime) < CACHE_TIME


def get_cache(url):
    ''' Return cache data if any.
    '''

    cache = b''
    url_hash = get_url_cache(url)
    cache_dir = get_cache_directory()
    if cache_dir.exists():
        cache_path = cache_dir / url_hash
        if cache_path.exists() and is_valid(cache_path):
            with cache_path.open('rb') as cache_file:
                cache = cache_file.read()

    return cache

def get_page_source(url, refresh=False):
    '''Get the html-page at the specified url address.
    '''

    cache = get_cache(url)
    if cache and not refresh:
        page = cache
    else:
        headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64;)'}
        page = requests.get(url, headers=headers)
        page = page.content
        save_cache(url, page)
    return page.decode('utf-8')


def get_locations(locations_url, refresh=False):
    '''
    Choosing a place for which you need to get weather information.
    '''

    soup = BeautifulSoup(get_page_source(locations_url,
                                         refresh=refresh), 'html.parser')
    locations = []

    for location in soup.find_all('li', attrs={'class': 'drilldown cl'}):
        url = location.find('a').get('href')
        location = location.find('em').get_text()
        locations.append((location, url))
    return locations


def get_configuration_file():
    '''The function returns the path to the configuration file.
    '''

    return Path.home() / CONFIG_FILE


def get_configuration():
    ''' The function returns data from the configuration file,
    if the file is configured, or accepts default data.
    '''

    name = DEFAULT_NAME
    url = DEFAULT_URL
    parser = configparser.ConfigParser()
    parser.read(get_configuration_file())

    if CONFIG_LOCATION in parser.sections():
        config = parser[CONFIG_LOCATION]
        name, url = config['name'], config['url']
    return name, url


def save_configuration(name, url):
    ''' Write the data received from the user (the city name and its URL)
     into the configuration file.
    '''

    parser = configparser.ConfigParser()
    parser[CONFIG_LOCATION] = {'name': name, 'url': url}
    with open(get_configuration_file(), 'w') as configfile:
        parser.write(configfile)


def configurate(refresh=False):
    ''' The user chooses the city for which he wants to get the weather.
    '''

    locations = get_locations(ACCU_BROWSE_LOCATIONS, refresh=refresh)
    while locations:
        for index, location in enumerate(locations):
            #print(f'{index + 1}. {location[0]}')
            print("{}. {}".format((index + 1), (location[0])))
        selected_index = int(input('Please select location: '))
        location = locations[selected_index - 1]
        locations = get_locations(location[1], refresh=refresh)

    save_configuration(*location)


def get_locations_rp5(locations_url, refresh=False):
    ''' Choosing a place for which you need to get weather information.
    '''

    soup = BeautifulSoup(get_page_source(locations_url, refresh=refresh),
                         'html.parser')
    locations = []
    for location in soup.find_all("h3"):
        url = location.find("a", class_="href20").get('href')
        if url[0] != '/':  # add '/' if it is missing from the url address
            url = '/' + url[:]
            location = location.find("a", class_="href20").get_text()
            locations.append((location, url))
        else:
            location = location.find("a", class_="href20").get_text()
            locations.append((location, url))
    return locations


def get_configuration_file_rp5():
    '''The function returns the path to the configuration file.
    '''

    return Path.home() / CONFIG_FILE_RP5


def get_configuration_rp5():
    ''' The function returns data from the configuration file,
    if the file is configured, or accepts default data.
    '''

    name = DEFAULT_NAME_RP5
    url = DEFAULT_URL_RP5
    parser = configparser.ConfigParser()
    parser.read(get_configuration_file_rp5())

    if CONFIG_LOCATION in parser.sections():
        config = parser[CONFIG_LOCATION]
        name, url = config['name'], 'http://rp5.ua' + config['url']
    return name, url


def save_configuration_rp5(name, url):
    ''' Write the data received from the user (the city name and its URL)
    into the configuration file.
    '''

    parser = configparser.ConfigParser()
    parser[CONFIG_LOCATION] = {'name': name, 'url': url}
    with open(get_configuration_file_rp5(), 'w') as configfile:
        parser.write(configfile)


def configurate_rp5(refresh=False):
    ''' The user chooses the city for which he wants to get the weather.
    '''

    soup = BeautifulSoup(get_page_source(RP5_BROWSE_LOCATIONS,
                                         refresh=refresh), 'html.parser')
    country_link = soup.find_all(class_="country_map_links")
    list_country = []
    for link in country_link:
        url = link.find(["a", "span"]).get('href')
        link = link.find(["a", "span"]).get_text()
        list_country.append((link, url))
    for index, location in enumerate(list_country):
        print("{}. {}".format((index + 1), (location[0])))
    index_country = int(input('Please select country location: '))
    link_country = list_country[index_country - 1]
    country_url = 'http://rp5.ua' + link_country[1]
    locations = get_locations_rp5(country_url, refresh=refresh)
    while locations:
        for index, location in enumerate(locations):
            print("{}. {}".format((index + 1), (location[0])))
        selected_index = int(input('Please select location: '))
        location = locations[selected_index - 1]
        city_url = 'http://rp5.ua' + location[1]
        locations = get_locations_rp5(city_url, refresh=refresh)

    save_configuration_rp5(*location)


def get_accu_weather(get_page, refresh=False):
    ''' The function returns a list with the values ​​of the state
        of the weather.
    '''

    weather_info = {}  # create a blank dictionary to enter the weather data

    # find the <div> container with the information we need
    soup = BeautifulSoup(get_page, 'html.parser')
    tag_container = soup.find(class_="day current first cl")
    if tag_container:
        current_day_url = tag_container.find('a').attrs['href']
        if current_day_url:
            current_day = get_page_source(current_day_url, refresh=refresh)
            current_day_page = BeautifulSoup(current_day, 'html.parser')
            if current_day_page:
                weather_details = current_day_page.find(id="detail-now")
                temp_info = weather_details.find('span', class_="large-temp")
                if temp_info:
                    weather_info['Temperature: '] = temp_info.get_text()
                realfeel = weather_details.find(class_="small-temp")
                if realfeel:
                    weather_info['Realfeel: '] = realfeel.get_text()
                cond = weather_details.find('span', class_="cond")
                if cond:
                    weather_info['Condition: '] = cond.get_text()

    return weather_info


def get_rp5_weather(get_page):
    '''The function returns a list with the values ​​of the state of the weather.
    '''

    weather_info = {}  # create a blank dictionary to enter the weather data
    soup = BeautifulSoup(get_page, 'html.parser')
    tag_container = soup.find(id="archiveString")
    if tag_container:
        forecast_temp = tag_container.find(id="ArchTemp")
        if forecast_temp:
            temp_info = forecast_temp.find(class_="t_0").get_text()
            weather_info['Temperature: '] = temp_info

        forecast_realfeel = tag_container.find(class_="TempStr")
        if forecast_realfeel:
            realfeel = forecast_realfeel.find(class_="t_0").get_text()
            weather_info['Realfeel: '] = realfeel

    forecast_string = soup.find(id="forecastShort-content").get_text()
    if forecast_string:
        lst_forecast = forecast_string.split(',')
        cond = lst_forecast[2]
        weather_info['Condition: '] = cond
    return weather_info


def output(city_name, info):
    ''' Displays the result of the received values ​​of the state of the weather.
    '''

    print("{}".format(city_name).center(20, '='))
    for key, value in info.items():
        print(key, value)
    print('\n')


def get_accu_weather_info(refresh=False):
    '''Displays the weather data for the specified city from the configuration file to the screen.
    '''

    city_name, city_url = get_configuration()
    content = get_page_source(city_url, refresh=refresh)
    output(city_name, get_accu_weather(content, refresh=refresh))


def get_rp5_weather_info(refresh=False):
    '''Displays the weather data for the specified city from the configuration file to the screen.
    '''

    city_name, city_url = get_configuration_rp5()
    content = get_page_source(city_url, refresh=refresh)
    output(city_name, get_rp5_weather(content))


def get_accu_info():
    get_page = get_page_source(ACCU_URL)
    accu_info = get_accu_weather(get_page)
    return accu_info


def get_rp5_info():
    get_page = get_page_source(RP5_URL)
    rp5_info = get_rp5_weather(get_page)
    return rp5_info


def writer_file_in_csv(refresh=False):
    '''write data in file format .csv'''

    data = [get_accu_info(), get_rp5_info()]
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
        output('Accuwether', get_accu_info())
        output('Rp5', get_rp5_info())


if __name__ == "__main__":
    main(sys.argv[1:])
