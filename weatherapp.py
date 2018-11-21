#!/usr/bin/python3

import requests, html
def weather(url, *args):
    '''Програма виводить значення температури і погодні умови із сайту accuweather.
    '''
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64;)'}
    accu_page = requests.get(url, headers = headers)
    accu_page = str(accu_page.text)
    ACCU_TEMP_TAG = ''
    for ACCU_TEMP_TAG in args:
        accu_temp_tag_size = len(ACCU_TEMP_TAG)
        accu_temp_tag_index = accu_page.find(ACCU_TEMP_TAG)
        accu_temp_value_start = accu_temp_tag_index + accu_temp_tag_size
        accu_temp = []
        for char in accu_page[accu_temp_value_start:]:
            if char != '<':
                accu_temp.append(char)
            else:
                break
        accu_temp = ''.join(accu_temp)
        print('{0:^25s}'.format(html.unescape(accu_temp)))

def rp5(rp_url, *args):
    '''Програма виводить значення температури і погодні умови із сайту rp5.ua
    '''
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64;)'}
    rp5 = requests.get(url, headers = headers)
    rp5_page = str(rp5_page.text)
    rp5_TEMP_TAG = ''
    for rp5_TEMP_TAG in args:
        rp5_temp_tag_size = len(rp5_TEMP_TAG)
        rp5_temp_tag_index = rp5_page.find(rp5_TEMP_TAG)
        rp5_temp_value_start = rp5_temp_tag_index + rp5_temp_tag_size
        rp5_temp = []
        for char in rp5_page[rp5_temp_value_start:]:
            if char != '<':
                rp5_temp.append(char)
            else:
                break
        rp5_temp = ''.join(rp5_temp)
        print('{0:<10s}'.format(html.unescape(rp5_temp)))

url = ('https://www.accuweather.com/uk/ua/brody/324506/weather-forecast/324506')

args = ('<span class="large-temp">', '<span class="cond">')
print("Accuweather: ")
weather(url, *args)

rp_url = ('http://rp5.ua/%D0%9F%D0%BE%D0%B3%D0%BE%D0%B4%D0%B0_%D0%B2_%D0%91%D1%80%D0%BE%D0%B4%D0%B0%D1%85,_%D0%9B%D1%8C%D0%B2%D1%96%D0%B2%D1%81%D1%8C%D0%BA%D0%B0_%D0%BE%D0%B1%D0%BB%D0%B0%D1%81%D1%82%D1%8C')
args = ('<span class="t_0" style="display: block;">', '<div class="cn4" onmouseover="tooltip(this, \'<b>')
print("Rp5.ua: ")
weather(rp_url, *args)

