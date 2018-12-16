import time

import hashlib

import configparser

import re

from pathlib import Path

import requests

from bs4 import BeautifulSoup

import config


class AccuWeatherProvider(object):
    ''' Weather provider for AccuWeather site.
    '''

    def __init__(self):
        self.name = config.ACCU_PROVIDER_NAME

        location, url = self.get_configuration()
        self.location = location
        self.url = url

    def get_configuration_file(self):
        '''The function returns the path to the configuration file.
        '''

        return Path.home() / config.CONFIG_FILE

    def get_configuration(self):
        ''' The function returns data from the configuration file,
        if the file is configured, or accepts default data.
        '''

        parser = configparser.ConfigParser()
        parser.read(self.get_configuration_file())

        if config.CONFIG_LOCATION in parser.sections():
            locatoin_config = parser[config.CONFIG_LOCATION]
            name, url = locatoin_config['name'], locatoin_config['url']
        else:
            name = config.DEFAULT_NAME
            url = config.DEFAULT_URL
        return name, url

    def save_configuration(self, name, url):
        ''' Write the data received from the user (the city name and its URL)
        into the configuration file.
        '''

        parser = configparser.ConfigParser()
        parser[config.CONFIG_LOCATION] = {'name': name, 'url': url}
        with open(self.get_configuration_file(), 'w') as configfile:
            parser.write(configfile)

    def get_url_cache(self, url):
        ''' Generates hash for given url.
        '''

        return hashlib.md5(url.encode('utf-8')).hexdigest()

    def get_cache_directory(self):
        '''The function returns the path to the cache directory.
        '''

        return Path.home() / config.CACHE_DIR

    def remove_cache(self, clear_cache=False):
        ''' Remove cache directory.
        '''

        cache_dir = self.get_cache_directory()
        if cache_dir.exists():
            for current_file in cache_dir.iterdir():
                current_file.unlink()  # To delete a folder you must first
                                       # delete all the files inside
            cache_dir.rmdir()

    def save_cache(self, url, page):
        ''' Save page source by given url address.
        '''

        url_hash = self.get_url_cache(url)
        cache_dir = self.get_cache_directory()
        if not cache_dir.exists():
            cache_dir.mkdir(parents=True)

        with (cache_dir / url_hash).open('wb') as cache_file:
            cache_file.write(page)

    def is_valid(self, path):
        '''Check if current cache file is valid.
        '''

        return (time.time() - path.stat().st_mtime) < config.CACHE_TIME

    def get_cache(self, url):
        ''' Return cache data if any.
        '''

        cache = b''
        url_hash = self.get_url_cache(url)
        cache_dir = self.get_cache_directory()
        if cache_dir.exists():
            cache_path = cache_dir / url_hash
            if cache_path.exists() and self.is_valid(cache_path):
                with cache_path.open('rb') as cache_file:
                    cache = cache_file.read()
        return cache

    def get_page_source(self, url, refresh=False):
        '''Get the html-page at the specified url address.
        '''

        cache = self.get_cache(url)
        if cache and not refresh:
            page = cache
            print(url)
        else:
            headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64;)'}
            page = requests.get(url, headers=headers)
            page = page.content
            self.save_cache(url, page)
        return page.decode('utf-8')

    def get_locations(self, locations_url, refresh=False):
        ''' Choosing a place for which you need to get weather information.
        '''

        soup = \
            BeautifulSoup(self.get_page_source\
                (locations_url, refresh=refresh), 'html.parser')
        locations = []

        for location in soup.find_all('li', attrs={'class': 'drilldown cl'}):
            url = location.find('a').get('href')
            location = location.find('em').get_text()
            locations.append((location, url))
        return locations

    def configurate(self, refresh=False):
        ''' The user chooses the city for which he wants to get the weather.
        '''

        locations = self.\
                get_locations(config.ACCU_BROWSE_LOCATIONS, refresh=refresh)
        while locations:
            for index, location in enumerate(locations):
                #print(f'{index + 1}. {location[0]}')
                print("{}. {}".format((index + 1), (location[0])))
            selected_index = int(input('Please select location: '))
            location = locations[selected_index - 1]
            locations = self.get_locations(location[1], refresh=refresh)

        self.save_configuration(*location)

    def get_accu_weather(self, refresh=False):
        ''' The function returns a list with the values the state the weather.
        '''

        weather_info = {}  # create a blank dictionary to enter the weather data

        # find the <div> container with the information we need
        soup = BeautifulSoup(self.get_page_source(self.url, refresh=refresh),\
                                                  'html.parser')
        tag_container = \
            soup.find(class_=re.compile("(day|night) current first cl"))
        if tag_container:
            current_day_url = tag_container.find('a').attrs['href']
            if current_day_url:
                current_day = self.get_page_source(current_day_url, refresh=refresh)
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

    def run(self, refresh=False):
        ''' The main command to launch your provider.
        '''
        content = self.get_page_source(self.url, refresh=refresh)
        return self.get_accu_weather(content)


class Rp5WeatherProvider(AccuWeatherProvider):
    ''' Weather provider for Rp5 site.
    '''

    def __init__(self):
        AccuWeatherProvider.__init__(self) # call the special method __init__ base class
        self.name = config.RP5_PROVIDER_NAME

        location, url = self.get_configuration_rp5()
        self.location = location
        self.url = url

    def get_locations_rp5(self, locations_url, refresh=False):
        ''' Choosing a place for which you need to get weather information.
        '''

        soup = BeautifulSoup(self.get_page_source(locations_url,\
                             refresh=refresh), 'html.parser')
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

    def get_configuration_file_rp5(self):
        '''The function returns the path to the configuration file.
        '''

        return Path.home() / config.CONFIG_FILE_RP5

    def get_configuration_rp5(self):
        ''' The function returns data from the configuration file,
        if the file is configured, or accepts default data.
        '''

        name = config.DEFAULT_NAME_RP5
        url = config.DEFAULT_URL_RP5
        parser = configparser.ConfigParser()
        parser.read(self.get_configuration_file_rp5())

        if config.CONFIG_LOCATION in parser.sections():
            location_config = parser[config.CONFIG_LOCATION]
            name, url = location_config['name'], 'http://rp5.ua' + location_config['url']
        return name, url


    def save_configuration_rp5(self, name, url):
        ''' Write the data received from the user (the city name and its URL)
        into the configuration file.
        '''

        parser = configparser.ConfigParser()
        parser[config.CONFIG_LOCATION] = {'name': name, 'url': url}
        with open(self.get_configuration_file_rp5(), 'w') as configfile:
            parser.write(configfile)

    def get_url_cache(self, url):
        ''' Generates hash for given url.
        '''

        return hashlib.md5(url.encode('utf-8')).hexdigest()

    def get_cache_directory(self):
        '''The function returns the path to the cache directory.
        '''

        return Path.home() / config.CACHE_DIR

    def configurate_rp5(self, refresh=False):
        ''' The user chooses the city for which he wants to get the weather.
        '''

        soup = BeautifulSoup(self.\
            get_page_source(config.RP5_BROWSE_LOCATIONS, refresh=refresh),\
                                                         'html.parser')
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
        locations = self.get_locations_rp5(country_url, refresh=refresh)
        while locations:
            for index, location in enumerate(locations):
                print("{}. {}".format((index + 1), (location[0])))
            selected_index = int(input('Please select location: '))
            location = locations[selected_index - 1]
            city_url = 'http://rp5.ua' + location[1]
            locations = self.get_locations_rp5(city_url, refresh=refresh)

        self.save_configuration_rp5(*location)


    def get_rp5_weather(self, refresh=False):
        '''The function returns a list with the value the state of the weather.
        '''

        weather_info = {}  # create a blank dictionary to enter the weather data
        soup = BeautifulSoup(self.get_page_source(self.url, refresh=refresh), 'html.parser')
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

    def run(self, refresh=False):
        content = self.get_page_source(self.url, refresh=refresh)
        return self.get_rp5_weather(content)


# def configurate_sinoptik(refresh=False):
#     ''' The user chooses the city for which he wants to get the weather.
#     '''
#     # find continent
#     soup = BeautifulSoup(get_page_source(config.SINOPTIK_BROWSE_LOCATIONS,\
#                                          refresh=refresh), 'html.parser')
#     container_continent = soup.find('div', attrs={'style': 'font-size:12px;'})
#     continent_link = container_continent.find_all("a")
#     list_continent = []
#     for link in continent_link:
#         url = link.get('href')
#         location = link.get_text()
#         list_continent.append((location, url))
#     for index, location in enumerate(list_continent):
#         print("{}. {}".format((index + 1), (location[0])))
#     index_continent = int(input('Please select continent location: '))
#     link_continent = list_continent[index_continent - 1]
#     country_url = 'http:' + link_continent[1]

#     # find counrty
#     country_tag = BeautifulSoup\
#                 (get_page_source(country_url, refresh=refresh), 'html.parser')
#     container_country = country_tag.find(class_="maxHeight")
#     country_link = container_country.find_all("a")
#     list_country = []
#     for link in country_link:
#         url = link.get('href')
#         location = link.get_text()
#         list_country.append((location, url))
#     for index, location in enumerate(list_country):
#         print("{}. {}".format((index + 1), (location[0])))
#     index_country = int(input('Please select country location: '))
#     link_country = list_country[index_country - 1]
#     city_url = 'http:' + link_country[1]
#     #print(locations)
#     # find city
#     locations = get_locations_sinoptik(city_url, refresh=refresh)

#     while locations:
#         for index, location in enumerate(locations):
#             print("{}. {}".format((index + 1), (location[0])))
#         selected_index = int(input('Please select location: '))
#         location = locations[selected_index - 1]
#         city_url = 'http:' + location[1]
#         locations = get_locations_sinoptik(city_url, refresh=refresh)
#     return locations

#     # self.save_configuration_rp5(*location)


# def get_sinoptik_weather(refresh=False):
#     '''The function returns a list with the value the state of the weather.
#     '''
#     weather_info = {}  # create a blank dictionary to enter the weather data
#     soup = BeautifulSoup(get_page_source(url, refresh=refresh), 'html.parser')
#     container_tag = soup.find(id="bd1c")
#     if container_tag:
#         today_temp = container_tag.find("p", class_="today-temp").get_text()
#         if today_temp:
#             weather_info['Temperature: '] = today_temp
#         img_text = container_tag.find("img").attrs["alt"]
#         if img_text:
#             weather_info['Condition: '] = img_text

#     return weather_info

# configurate_sinoptik(refresh=False)
