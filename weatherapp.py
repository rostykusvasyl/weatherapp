#!/usr/bin/python3

import requests, html


accu_url = ('https://www.accuweather.com/uk/ua/brody/324506/weather-forecast/324506')
accu_tags = ('<span class="large-temp">', '<span class="cond">')
rp5_url = ('http://rp5.ua/%D0%9F%D0%BE%D0%B3%D0%BE%D0%B4%D0%B0_%D0%B2_%D0%91%D1%80%D0%BE%D0%B4%D0%B0%D1%85,'
            '_%D0%9B%D1%8C%D0%B2%D1%96%D0%B2%D1%81%D1%8C%D0%BA%D0%B0_%D0%BE%D0%B1%D0%BB%D0%B0%D1%81%D1%82%D1%8C')
rp5_tags = ('<span class="t_0" style="display: block;">',
            '<div class="cn6" onmouseover="tooltip(this, \'<b>')

container_tags = '<td colspan="2" class="n"> <div class="cc_0">'


# url = ('https://ua.sinoptik.ua/%D0%BF%D0%BE%D0%B3%D0%BE%D0%B4%D0%B0-%D0%B1%D1%80%D0%BE%D0%B4%D0%B8')
# args = ('<p class="today-temp">', '<div class="weatherIco d400" title=')
# print("Sinoptik.ua: ")
# weather(url, *args)

def get_page(url):
    '''Функція повертає строкові дані з веб сторінки, вказаній в url адресі
    '''
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64;)'}
    html_page = requests.get(url, headers = headers)
    return html_page.text


def get_weather_info(get_page, tags):
    '''Функція повертає кортеж із значеннями про стан погоди для заданих тегів
    '''
    def get_tag_content(get_page, tag):
        '''Отримуємо інформацію із веб сторінки про стан погоди для заданого тегу
        '''
        container_tags = '<div id="forecastShort-content">'
        tag_index = get_page.find(tag, get_page.find(container_tags))
        print(tag_index)
        tag_size = len(tag)
        value_start = tag_index + tag_size
        content = ''
        for char in get_page[value_start:]:
            if char != '<' and char != '>':
                content += char
            else:
                break
        return content
    return tuple([get_tag_content(get_page, tag) for tag in tags])


def output(name, temp, condition, leftWidth=12, rightWidth=10):
    '''Виводимо на екран результат отриманих значень про стан погоди із вказаних сайтів
    '''
    print(f"{name}".center(30, '='))
    print(f"Temperature: {html.unescape(temp)}".ljust(30))
    print(f"Condition: {condition}", end="\n\n")


def main():
    '''Main entry point in program.
    '''
    weather_sites = {'Accuweather': (accu_url, accu_tags),
                    'Rp5': (rp5_url, rp5_tags)}

    for name in weather_sites:
        url, tags = weather_sites[name]
        content = get_page(url)
        temp, condition = get_weather_info(content, tags)
        output(name, temp, condition)


if __name__ == "__main__":
    main()