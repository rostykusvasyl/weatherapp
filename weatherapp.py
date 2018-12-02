#! /usr/bin/env python3

'''Program for web-scraping of weather sites'''

import argparse

import sys

import csv

import requests

from bs4 import BeautifulSoup





accu_url = ('https://www.accuweather.com/uk/ua/brody/324506/current-weather/324506')


rp5_url = ('http://rp5.ua/%D0%9F%D0%BE%D0%B3%D0%BE%D0%B4%D0%B0_%D0%'
           'B2_%D0%91%D1%80%D0%BE%D0%B4%D0%B0%D1%85,_%D0%9B%D1%8C%'
           'D0%B2%D1%96%D0%B2%D1%81%D1%8C%D0%BA%D0%'
           'B0_%D0%BE%D0%B1%D0%BB%D0%B0%D1%81%D1%82%D1%8C')


# sinoptik_url = ('https://ua.sinoptik.ua/%D0%BF%D0%BE%D0%B3%D0%BE%D0%B4%D0%'
#        'B0-%D0%B1%D1%80%D0%BE%D0%B4%D0%B8')


def get_weather_info(url):
    '''Функція повертає список із значеннями про стан погоди
    '''
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64;)'}
    page = requests.get(url, headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser')

    weather_info = {}  # створюємо пустий словник
                       # для внесення даних про стан погоди

    tag_container = soup.find(id="detail-now")  # знаходимо на сторінці
                                                # <div>-контейнер з потрібною
                                                # нам інформацією
    forecast = tag_container.find(class_="info")
    temp_info = forecast.find(class_="large-temp").get_text()
    weather_info['Temperature: '] = temp_info

    realfeel = forecast.find(class_="small-temp").get_text()
    weather_info['Realfeel: '] = realfeel

    cond = forecast.find(class_="cond").get_text()
    weather_info['Condition: '] = cond

    return weather_info


def get_weather_info_rp5(url):
    '''Функція повертає список із значеннями про стан погоди'''
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64;)'}
    page = requests.get(url, headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser')
    weather_info = {}  # створюємо пустий словник
                       #для внесення даних про стан погоди
    tag_container = soup.find(id="archiveString")  # знаходимо на сторінці
                                                   # <div>-контейнер з
                                                   #потрібною нам інформацією

    forecast_temp = tag_container.find(id="ArchTemp")
    temp_info = forecast_temp.find(class_="t_0").get_text()
    weather_info['Temperature: '] = temp_info


    forecast_realfeel = tag_container.find(class_="TempStr")
    realfeel = forecast_realfeel.find(class_="t_0").get_text()
    weather_info['Realfeel: '] = realfeel

    forecast_string = soup.find(id="forecastShort-content").get_text()
    lst_forecast = forecast_string.split(',')
    cond = lst_forecast[2]
    weather_info['Condition: '] = cond
    return weather_info

def output(name, info):
    '''Виводимо на екран результат
       отриманих значень про стан погоди
    '''
    print(name.center(20, '='))
    for key, value in info.items():
        print(key, value)
    print('\n')


def output_csv(name, info):
    '''write file in .csv format'''
    data = []
    data.append(info)
    with open('csv_weather.csv', 'at') as frecord:
        frecord.write(name + '\n')
        writer = csv.DictWriter(frecord, fieldnames=list(data[0].keys()))
        writer.writeheader()
        writer.writerows(data)


def main(argv):
    '''Main entry point in program.
    '''
    command_list = {'accu': 'Accuweather', 'rp5': 'Rp5', 'csv': 'csv'}

    parser = argparse.ArgumentParser(prog='PROG_WEATHER',
                                     description='Displaying weather information.')

    parser.add_argument('--version', action='version', version='%(prog)s 0.0.1')
    parser.add_argument('command', help='Enter "accu" for the '
                        'Accuwether website or "rp5" for the '
                        'Rp5 site.', nargs='*')
    args = parser.parse_args(argv)
    weather_sites = {'Accuweather': accu_url, 'Rp5': rp5_url, 'csv': 'csv'}

    if args.command:
        command = args.command[0]
        if command in command_list:
            weather_sites = {command_list[command]: weather_sites[command_list[command]]}
            if command == 'accu':
                name = 'Accuweather'
                url = weather_sites[name]
                accu_info = get_weather_info(url)
                output(name, accu_info)
            elif command == 'rp5':
                name = 'Rp5'
                url = weather_sites[name]
                rp5_info = get_weather_info_rp5(url)
                output(name, rp5_info)
            elif command == 'csv':
                accu_info = get_weather_info(accu_url)
                output_csv('Accuweather', accu_info)
                rp5_info = get_weather_info_rp5(rp5_url)
                output_csv('Rp5', rp5_info)
        else:
            print('Unknown command provided!')
            sys.exit(1)
    else:
        accu_info = get_weather_info(accu_url)
        output('Accuweather', accu_info)
        rp5_info = get_weather_info_rp5(rp5_url)
        output('Rp5', rp5_info)



if __name__ == "__main__":
    main(sys.argv[1:])
