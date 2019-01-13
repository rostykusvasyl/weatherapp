""" Weather providers.
"""

import re
from pathlib import Path
from bs4 import BeautifulSoup
from abstract import WeatherProvider

import config


class AccuProvider(WeatherProvider):
    """ Weather provider for AccuWeather site.
    """

    name = config.ACCU_PROVIDER_NAME
    title = config.ACCU_PRVIDER_TITLE

    def get_default_location(self):
        """ Default location name.
        """

        return config.DEFAULT_ACCU_LOCATION_NAME

    def get_default_url(self):
        """ Default location url.
        """
        return config.DEFAULT_ACCU_LOCATION_URL

    def get_name(self):
        """ Get name provider
        """
        return self.name

    def get_locations(self, locations_url):
        """ Choosing a place for which you need to get weather information.
        """

        soup = \
            BeautifulSoup(self.get_page_source(locations_url), 'html.parser')
        locations = []

        for location in soup.find_all('li', attrs={'class': 'drilldown cl'}):
            url = location.find('a').get('href')
            location = location.find('em').get_text()
            locations.append((location, url))
        return locations

    def configurate(self):
        """ The user chooses the city for which he wants to get the weather.
        """

        locations = self.get_locations(config.ACCU_BROWSE_LOCATIONS)
        while locations:
            for index, location in enumerate(locations):
                print("{}. {}".format((index + 1), (location[0])))
            while True:
                try:
                    selected_index = int(input('Please select location'
                                         '(in format integer number): '))
                    if selected_index > 0:
                        location = locations[selected_index - 1]
                        break
                except ValueError:
                    print("That was no valid number. Try again...")
                except IndexError:
                    print("This number out of range. Try again...")

            locations = self.get_locations(location[1])

            self.save_configuration(*location)

    def get_weather_info(self, page):
        """ The function returns a list with the values the state the weather.
        """
        # create a blank dictionary to enter the weather data
        weather_info = {}

        # find the <div> container with the information we need
        soup = BeautifulSoup(page, 'html.parser')
        tag_container = \
            soup.find(class_=re.compile("(day|night) current first cl"))
        if tag_container:
            current_day_url = tag_container.find('a').attrs['href']
            if current_day_url:
                current_day = self.get_page_source(current_day_url)
                current_day_page = BeautifulSoup(current_day, 'html.parser')
                if current_day_page:
                    weather_details = current_day_page.find(id="detail-now")
                    temp_info = weather_details.find('span',
                                                     class_="large-temp")
                    if temp_info:
                        weather_info['Temperature: '] = temp_info.get_text()
                    realfeel = weather_details.find(class_="small-temp")
                    if realfeel:
                        weather_info['Realfeel: '] = realfeel.get_text()
                    cond = weather_details.find('span', class_="cond")
                    if cond:
                        weather_info['Condition: '] = cond.get_text()
                return weather_info


class Rp5Provider(WeatherProvider):
    """ Weather provider for rp5.ua site.
    """

    name = config.RP5_PROVIDER_NAME
    title = config.RP5_PROVIDER_TITLE

    def get_default_location(self):
        """ Default location name.
        """
        return config.DEFAULT_RP5_LOCATION_NAME

    def get_default_url(self):
        """ Default location url.
        """
        return config.DEFAULT_RP5_LOCATION_URL

    def get_name(self):
        """ Get name provider
        """
        return self.name

    def _get_configuration_file(self):
        """ The function returns the path to the configuration file.
        """

        return Path.home() / config.CONFIG_FILE

    def get_locations_region(self, locations_url):
        """ Choosing a place for which you need to get weather information.
        """

        soup = BeautifulSoup(
            self.get_page_source(locations_url), 'html.parser')
        locations = []
        for location in soup.find_all("h3"):
            url = \
                'http://rp5.ua/' + location.find("a", class_="href20").get('href')
            location = location.find("a", class_="href20").get_text()
            locations.append((location, url))
        return locations

    def configurate(self):
        """ The user chooses the city for which he wants to get the weather.
        """

        # Find country
        soup = BeautifulSoup(
            self.get_page_source(config.RP5_BROWSE_LOCATIONS), 'html.parser')
        country_link = soup.find_all(class_="country_map_links")
        list_country = []
        for link in country_link:
            url = link.find(["a", "span"]).get('href')
            link = link.find(["a", "span"]).get_text()
            list_country.append((link, url))
        for index_country, location in enumerate(list_country):
            print("{}. {}".format((index_country + 1), (location[0])))
        while True:
            try:
                index_country = \
                    int(input('Please select country location: '))
                if index_country > 0:
                    link_country = list_country[index_country - 1]
                    break
            except ValueError:
                print("That was no valid number. Try again...")
            except IndexError:
                print("This number out of range. Try again...")

        country_url = 'http://rp5.ua' + link_country[1]

        # Find region
        locations = self.get_locations_region(country_url)
        for index_region, location in enumerate(locations):
            print("{}. {}".format((index_region + 1), (location[0])))
        while True:
            try:
                index_region = int(input('Please select location: '))
                if index_region > 0:
                    region = locations[index_region - 1]
                    break
            except ValueError:
                print("That was no valid number. Try again...")
            except IndexError:
                print("This number out of range. Try again...")

        region_url = region[1]

        # Find city
        city_location = \
            BeautifulSoup(self.get_page_source(region_url), 'html.parser')
        list_city = []
        tag_container = city_location.find_all(class_="city_link")
        if tag_container:
            for location in tag_container:
                url = 'http://rp5.ua/' + location.find("a").get('href')
                location = location.find("a").get_text()
                list_city.append((location, url))
            for index_city, location in enumerate(list_city):
                print("{}. {}".format((index_city + 1), (location[0])))
            while True:
                try:
                    index_city = int(input('Please select city: '))
                    if index_city > 0:
                        city = locations[index_city - 1]
                        break
                except ValueError:
                    print("That was no valid number. Try again...")
                except IndexError:
                    print("This number out of range. Try again...")

            self.save_configuration(*city)
        else:
            self.save_configuration(*region)

    @staticmethod
    def get_weather_info(page):
        """ The function returns a list with the value the state of the weather.
        """

        # create a blank dictionary to enter the weather data
        weather_info = {}
        soup = BeautifulSoup(page, 'html.parser')
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


class SinoptikProvider(WeatherProvider):
    """ Weather provider for AccuWeather site.
    """

    name = config.SINOPTIK_PROVIDER_NAME
    title = config.SINOPTIK_PROVIDER_TITLE

    def get_default_location(self):
        """ Default location name.
        """
        return config.DEFAULT_SINOPTIK_LOCATION_NAME

    def get_default_url(self):
        """ Default location url.
        """
        return config.DEFAULT_SINOPTIK_LOCATION_URL

    def get_name(self):
        """ Get name provider
        """
        return self.name

    def _get_configuration_file(self):
        """ The function returns the path to the configuration file.
        """

        return Path.home() / config.CONFIG_FILE

    def get_link_continent(self):
        """ Get location country.
        """

        soup = BeautifulSoup(
                self.get_page_source(config.SINOPTIK_BROWSE_LOCATIONS),
                'html.parser')
        container_continent = \
            soup.find('div', attrs={'style': 'font-size:12px;'})
        continent_link = container_continent.find_all("a")
        list_continent = []
        for link in continent_link:
            url = link.get('href')
            location = link.get_text()
            list_continent.append((location, url))
        return list_continent

    def get_link_country(self, location_url):
        """ Get location city.
        """

        country_tag = \
            BeautifulSoup(self.get_page_source(location_url), 'html.parser')
        container_city = country_tag.find(class_="maxHeight")
        city_link = container_city.find_all("a")
        list_country = []
        for link in city_link:
            url = link.get('href')
            location = link.get_text()
            list_country.append((location, url))
        return list_country

    def configurate(self):
        """ The user chooses the city for which he wants to get the weather.
        """
        # Find continent
        list_continent = self.get_link_continent()
        for index, location in enumerate(list_continent):
            print("{}. {}".format((index + 1), (location[0])))
        while True:
            try:
                index_continent =\
                    int(input('Please select continent location: '))
                if index_continent > 0:
                    link_continent = list_continent[index_continent - 1]
                    break
            except ValueError:
                print("That was no valid number. Try again...")
            except IndexError:
                print("This number out of range. Try again...")

        continent_url = 'http:' + link_continent[1]

        # find counrty
        list_country = self.get_link_country(continent_url)
        for index, location in enumerate(list_country):
            print("{}. {}".format((index + 1), (location[0])))
        while True:
            try:
                index_country =\
                    int(input('Please select country location: '))
                if index_country > 0:
                    link_country = list_country[index_country - 1]
                    break
            except ValueError:
                print("That was no valid number. Try again...")
            except IndexError:
                print("This number out of range. Try again...")

        country_url = 'http:' + link_country[1]

        # Find region
        list_region = self.get_link_country(country_url)
        for index, location in enumerate(list_region):
            print("{}. {}".format((index + 1), (location[0])))
        while True:
            try:
                index_region = int(input('Please select region location: '))
                if index_region > 0:
                    link_region = list_region[index_region - 1]
                    break
            except ValueError:
                print("That was no valid number. Try again...")
            except IndexError:
                print("This number out of range. Try again...")

        location_region = 'http:' + link_region[1]

        # Find city
        page_city = \
            BeautifulSoup(self.get_page_source(location_region), 'html.parser')
        container_tag = page_city.find(class_="mapBotCol")
        city_tag = container_tag.find(class_="clearfix")
        list_city = []
        for link in city_tag.find_all('a'):
            url = 'http:' + link.get('href')
            location = link.get_text()
            list_city.append((location, url))
        for index, location in enumerate(list_city):
            print("{}. {}".format((index + 1), (location[0])))
        while True:
            try:
                index_city = int(input('Please select city location: '))
                if index_city > 0:
                    city = list_city[index_city - 1]
                    break
            except ValueError:
                print("That was no valid number. Try again...")
            except IndexError:
                print("This number out of range. Try again...")

        self.save_configuration(*city)

    @staticmethod
    def get_weather_info(page):
        """ The function returns a list with the value the state of the weather.
        """

        # create a blank dictionary to enter the weather data
        weather_info = {}
        soup = BeautifulSoup(page, 'html.parser')
        container_tag = soup.find(id="bd1c")
        if container_tag:
            today_temp = container_tag.find("p", class_="today-temp").get_text()
            if today_temp:
                weather_info['Temperature: '] = today_temp
            img_text = container_tag.find("img").attrs["alt"]
            if img_text:
                weather_info['Condition: '] = img_text

        return weather_info
