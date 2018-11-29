#!/home/vasyl/StartDragon/weatherapp/bin/python3

from bs4 import BeautifulSoup
import requests, html


# accu_url = ('https://www.accuweather.com/uk/ua/brody/324506/'
#             'weather-forecast/324506')


url = ('http://rp5.ua/%D0%9F%D0%BE%D0%B3%D0%BE%D0%B4%D0%B0_%D0%'
             'B2_%D0%91%D1%80%D0%BE%D0%B4%D0%B0%D1%85,_%D0%9B%D1%8C%'
             'D0%B2%D1%96%D0%B2%D1%81%D1%8C%D0%BA%D0%'
            'B0_%D0%BE%D0%B1%D0%BB%D0%B0%D1%81%D1%82%D1%8C')


# sinoptik_url = ('https://ua.sinoptik.ua/%D0%BF%D0%BE%D0%B3%D0%BE%D0%B4%D0%'
#        'B0-%D0%B1%D1%80%D0%BE%D0%B4%D0%B8')


def get_page(url):
    '''завантажуємо HTML-вміст веб-сторінки з вказаної адреси
    '''
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64;)'}
    page  = requests.get(url, headers = headers)
    soup = BeautifulSoup(page.content, 'html.parser')
    return soup

get_page = get_page(url)
# def get_weather_info(get_page):
#     '''Функція повертає список із значеннями про стан погоди
#     '''
#     weather_info = {}  # створюємо пустий словник
#                        # для внесення даних про стан погоди
#     forecast = get_page.find(class_="bg bg-cl")  # знаходимо на сторінці
#                                                  # <div>-контейнер з потрібною
#                                                  # нам інформацією
#     temp_info = forecast.find(class_="large-temp").get_text()
#     weather_info['Temperature: '] = temp_info

#     realfeel = forecast.find(class_="realfeel").get_text()
#     weather_info['Realfeel: '] = realfeel

#     cond = forecast.find(class_="cond").get_text()
#     weather_info['Condition: '] = cond

#     return weather_info


def get_weather_info_rp5(get_page):
    '''Функція повертає список із значеннями про стан погоди
    '''
    weather_info = {}  # створюємо пустий словник
                       # для внесення даних про стан погоди
    forecast = get_page.find(class_="n underlineRow toplineRow blue")  # знаходимо на сторінці
                                                                  # <div>-контейнер з потрібною
                                                                  # нам інформацією
    temp_info = forecast.find(class_="t_0").get_text()
    weather_info['Temperature: '] = temp_info

    forecast_cond = get_page.find(id="ftab_1_content")
    cond = forecast_cond.find(colspan="2")

    print(cond)

# def output(name, info):
#     '''Виводимо на екран результат отриманих значень про стан погоди
#     '''
#     print(name.center(30, '='))
#     for k,v in info.items():
#         print(k, v)
#     print('\n')

get_weather_info_rp5(get_page)


# def main():
#     '''Main entry point in program.
#     '''
#     weather_sites = {'Accuweather: ': accu_url}

#     for name in weather_sites:
#         url= weather_sites[name]
#         content = get_page(url)
#         info = get_weather_info(content)
#         output(name, info)


# if __name__ == "__main__":
#     main()