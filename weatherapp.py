#!/usr/bin/python3

import requests, html
def weather(url, *args):
    '''Програма виводить значення температури і погодні умови із сайту accuweather.
    '''
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64;)'}
    html_page = requests.get(url, headers = headers)
    html_page = str(html_page.text)
    WINFO_TAG = ''
    for WINFO_TAG in args:
        winfo_tag_size = len(WINFO_TAG)
        winfo_tag_index = html_page.find(WINFO_TAG)
        winfo_value_start = winfo_tag_index + winfo_tag_size
        winfo = []
        for char in html_page[winfo_value_start:]:
            if char != '<' and char != '>':
                winfo.append(char)
            else:
                break
        winfo = ''.join(winfo)
        print('{0:^25s}'.format(html.unescape(winfo)))


url = ('https://www.accuweather.com/uk/ua/brody/324506/weather-forecast/324506')
args = ('<span class="large-temp">', '<span class="cond">')
print("Accuweather: ")
weather(url, *args)

url = ('http://rp5.ua/%D0%9F%D0%BE%D0%B3%D0%BE%D0%B4%D0%B0_%D0%B2_%D0%91%D1%80%D0%BE%D0%B4%D0%B0%D1%85,'
    '_%D0%9B%D1%8C%D0%B2%D1%96%D0%B2%D1%81%D1%8C%D0%BA%D0%B0_%D0%BE%D0%B1%D0%BB%D0%B0%D1%81%D1%82%D1%8C')
args = ('<span class="t_0" style="display: block;">', '<div class="cd7" onmouseover="tooltip(this, \'<b>')
print("Rp5.ua: ")
weather(url, *args)

url = ('https://ua.sinoptik.ua/%D0%BF%D0%BE%D0%B3%D0%BE%D0%B4%D0%B0-%D0%B1%D1%80%D0%BE%D0%B4%D0%B8')
args = ('<p class="today-temp">', '<div class="weatherIco d400" title=')
print("Sinoptik.ua: ")
weather(url, *args)