#!/usr/bin/python3

import requests, html


accu_url = ('https://www.accuweather.com/uk/ua/brody/324506/weather-forecast/324506')
accu_tags = ('<span class="large-temp">', '<span class="cond">')

rp5_url = ('http://rp5.ua/%D0%9F%D0%BE%D0%B3%D0%BE%D0%B4%D0%B0_%D0%B2_%D0%91%D1%80%D0%'
            'BE%D0%B4%D0%B0%D1%85,_%D0%9B%D1%8C%D0%B2%D1%96%D0%B2%D1%81%D1%8C%D0%BA%D0%'
            'B0_%D0%BE%D0%B1%D0%BB%D0%B0%D1%81%D1%82%D1%8C')
rp5_tags=('<span class="t_0" style="display: block;">','<div class="cn6" onmouseover="tooltip(this, \'<b>')


sinoptik_url = ('https://ua.sinoptik.ua/%D0%BF%D0%BE%D0%B3%D0%BE%D0%B4%D0%'
       'B0-%D0%B1%D1%80%D0%BE%D0%B4%D0%B8')
sinoptik_tags = ('<p class="today-temp">', '<div class="img"> <img width="188" height="150" src="//sinst.fwdcdn.com/img/weatherImg/b/n400.jpg" alt=')


container_tags = ('<div class="temp">', '<div id="ArchTemp">', '<div class="main loaded" id="bd1">',
                    '<p class="today-time">')

def get_page(url):
    '''Функція повертає строкові дані з веб сторінки, вказаній в url адресі
    '''
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64;)'}
    html_page = requests.get(url, headers = headers)
    return html_page.text


def get_weather_info(get_page, tags, container_tags):
    '''Функція повертає кортеж із значеннями про стан погоди для заданих тегів
    '''
    for cont_tag in container_tags:
        tag_info = []
        for tag in tags:
            if cont_tag in get_page and tag in get_page:
                tag_index = get_page.find(tag, get_page.find(cont_tag))
            else:
                tag_index = get_page.find(tag)
            tag_size = len(tag)
            value_start = tag_index + tag_size
            content = ''
            for char in get_page[value_start:]:
                if char != '<' and char != '>' and char != '/':
                    content += char
                else:
                    break
            tag_info.append(content)
    return tuple(tag_info)


def output(name, temp, condition):
    '''Виводимо на екран результат отриманих значень про стан погоди із вказаних сайтів
    '''
    print(f"{name}".center(len(condition) + len("Condition") + len("Condition") + len(name), '='))
    lst = {' Temperature: ': html.unescape(temp), '  Condition: ': condition}
    for k,v in lst.items():
        print(k, v.rjust(18, '.'))
    print('\n')


def main():
    '''Main entry point in program.
    '''
    weather_sites = {'Accuweather': (accu_url, accu_tags),
                    'Rp5': (rp5_url, rp5_tags),
                    'Sinoptik.ua': (sinoptik_url, sinoptik_tags)}

    for name in weather_sites:
        url, tags = weather_sites[name]
        content = get_page(url)
        temp, condition = get_weather_info(content, tags, container_tags)
        output(name, temp, condition)


if __name__ == "__main__":
    main()