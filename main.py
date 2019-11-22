import requests
from bs4 import BeautifulSoup as bs
from tkinter import *

headers = {
    'accept': '*/*',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/78.0.3904.97 Safari/537.36 '
}

base_url = 'https://yandex.ru/pogoda/saint-petersburg/details?via=ms'

flag = True


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
            fc_date = f'{a.text} {b.text}\n({c.text})'
            fc_dates.append(fc_date)

        # достаем список температуры утром, днем, вечером, ночью на 10 дней
        fc_temp_fdt = fc_det.find_all('div', attrs={'class': 'weather-table__temp'})
        fc_temps_ad = []
        fc_temps = {}
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

        for i in range(10):
            weekday_example = 'Утро\nДень\nВечер\nНочь'
            weekday = f'{fc_temps_ad[i]["morning"]}\n{fc_temps_ad[i]["day"]}\n{fc_temps_ad[i]["evening"]}\n' \
                      f'{fc_temps_ad[i]["night"]}'

            weekday_label = Label(root, text=weekday_example, font=("Arial", 15), borderwidth=2, relief="groove")
            weekday_label.grid(row=2, column=0, padx=15)
            Label(root, borderwidth=2, relief="groove", text=fc_dates[i], fg="#fff", bg="#222",
                  font=("Arial", 15), width=12).grid(row=1, column=i + 1, pady=10)
            Label(root, borderwidth=2, relief="groove", text=weekday, font=("Arial", 15),
                  width=12).grid(row=2, column=i + 1)

            # консольный вывод
            # output = f'{fc_dates[i]} \t- утром: {fc_temps_ad[i]["morning"]}\n\t\t\t\t' \
            #          f'\t\t- днем: {fc_temps_ad[i]["day"]}\n\t\t\t\t' \
            #          f'\t\t- вечером: {fc_temps_ad[i]["evening"]}\n\t\t\t\t' \
            #          f'\t\t- ночью: {fc_temps_ad[i]["night"]}\n\t'
            # print(output)

    else:
        # print('ERROR')
        Label(root, text='ERROR', bg="red", fg="#fff").grid(row=1, column=1, columnspan=2)


# удаление всех элементов окна кроме кнопки Обновить
def cleanup():
    to_delete_list = root.grid_slaves()
    for delete_item in to_delete_list:
        if (delete_item != updateButton) and (delete_item != copyLabel):
            delete_item.destroy()


def update_func():
    global flag
    if flag:
        weather_parse()
        flag = False
    else:
        cleanup()
        weather_parse()


root = Tk()
root.title('Парсер сайта Яндекс Погода')
root.geometry("1500x250")

updateButton = Button(root, text="Обновить", fg="#fff", bg="#0d801b", font=("Arial", 15), relief="flat",
                      command=update_func)
updateButton.grid(row=3, columnspan=2, column=0, pady=15, padx=20)

copyLabel = Label(root, text='GSK © 2019', font=("Arial", 15))
copyLabel.grid(row=3, columnspan=2, column=10, pady=15)

root.mainloop()
