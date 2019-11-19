import requests
from bs4 import BeautifulSoup as bs

headers = {
    'accept': '*/*',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36'
}

base_url = 'https://yandex.ru/pogoda/saint-petersburg/details?via=ms'


def weather_parse():
    session = requests.Session()
    request = session.get(base_url, headers=headers)

    if request.status_code == 200:

        soup = bs(request.content, "lxml")
        # forecast details
        # достаем див в котором хранятся все элементы с погодой
        fc_det = soup.find('div', attrs={'data-bem': '{"forecast-details":{"isCardView":true}}'})

        # достаем дни, месяца, название дня недели и создаем dict в котором хранится 10 ближайших дней
        fc_day = fc_det.find_all('strong', attrs={'class': 'forecast-details__day-number'})
        fc_month = fc_det.find_all('span', attrs={'class': 'forecast-details__day-month'})
        fc_weekday = fc_det.find_all('span', attrs={'class': 'forecast-details__day-name'})
        fc_dates = []
        for i in range(len(fc_day)):
            a, b, c = fc_day[i], fc_month[i], fc_weekday[i]
            fc_date = f'{a.text} {b.text} ({c.text})'
            fc_dates.append(fc_date)

            # тестовый вывод
            # print(fc_fd)
        # print(len(fc_dates))

        # достаем список температуры утром, днем, вечером, ночью на 10 дней
        fc_temp_fdt = fc_det.find_all('div', attrs={'class': 'weather-table__temp'})
        fc_temps_ad = []
        fc_temps = {}
        # k = 0
        for i in range(40):
            d = fc_temp_fdt[i]

            if i % 4 == 0:
                fc_temps.update({'morning': d.text})
            elif i % 4 == 1:
                fc_temps.update({'day': d.text})
            elif i % 4 == 2:
                fc_temps.update({'evening': d.text})
            else:
                fc_temps.update({'night': d.text})
                fc_temps_ad.append(fc_temps)
                fc_temps = {}
                # k += 1

        # тестовый вывод
        # print(len(fc_temps_ad))
        # # print(len(fc_temps_ad))
        # for t in fc_temps_ad:
        #     print(t)
        # for i in fc_temps:
        #     print(fc_temps[i])
        for i in range(10):
            output = f'{fc_dates[i]} \t- утром: {fc_temps_ad[i]["morning"]}\n\t\t\t\t' \
                     f'\t\t- днем: {fc_temps_ad[i]["day"]}\n\t\t\t\t' \
                     f'\t\t- вечером: {fc_temps_ad[i]["evening"]}\n\t\t\t\t' \
                     f'\t\t- ночью: {fc_temps_ad[i]["night"]}\n\t'
            print(output)

    else:
        print('ERROR')


weather_parse()
