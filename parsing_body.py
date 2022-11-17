import os
import pandas as pd
import requests
import re
import glob
import time
import json


group_ids = []
good_id_list = []
tokens_list = ['vk1.a.7PwF92LnqKGSBTPHjvIV5kSrnbLaO7Ozb3LLCIGRUlzRQfxnsmIsCfYt7tP4S6G7KM8fMNvQNwa0Xb5CHqoahJCcXA3lIOfmrPY6Y3MC9j1KwAWu9A0geh_UGUyLiMVmYbk__ExylGgiy2uiWscc7C4TPbDhs-GK391GZOQXQ0nLKN8QU1o1PxQx6TodoUUj',
               'vk1.a.3glTHF3apXS4DMSkaz-SBBkLWkWG1X2HUMHJcdcVVCLhRd1DTuU2_kh--bR9g73HPKd3JPLj1RZBUtA8wRX3XX7eYwrV1sG-jDPvCHMPspZoWORBfi95bGGvLo3Y-uDpdgyRPq9PtiqU0G7mZUc9eqysuy3jC2eEnr_YhUgGH_E81v_R8TPB_TWs2LMtATwM']
mobile_phone_list = []
home_phone_list = []
names_list = []
second_names_list = []
cities_list = []
bdate_list = []
group_name_list = []
group_id_list = []
date_list = []
logic_union_list = []
filename_list = []
insert = '''insert into static.parsing_vk(vk_id, mobile_phone, name, last_name, city, group_id, create_date, logic_union)
                                                        values {insert_here}'''
select = '''select *
                    from static.parsing_vk pv
                where pv.logic_union like '%{logic_union}%' '''

check_city_list = ['Новосибирск', 'Бердск', 'Искитим', 'Обь', 'Академгородок', 'Кольцово', 'Барнаул', 'Бийск',
                   'Рубцовск', 'Новоалтайск', 'Заринск', 'Новокузнецк', 'Междуреченск', 'Осинники', 'Калтан', 'Мыски',
                   'Прокопьевск', 'Киселевск', 'Кемерово', 'Берёзовский', 'Ленинск-Кузнецкий', 'Юрга',
                   'Анжеро-Судженск', 'Топки', 'Белово', 'Инской', 'Грамотеино', 'Гурьевск',  'Красноярск', 'Минусинск',
                   'Ачинск', 'Зеленогорск', 'Лесосибирск', 'Назарово', 'Железногорск', 'Дивногорск', 'Заозёрный',
                   'Бородино', 'Молодёжный', 'Абакан', 'Черногорск']


def get_phones(response):
    if 'mobile_phone' in response:
        if len(response['mobile_phone']) != 0:
            mobile_phone_list.append(response['mobile_phone'])
        else:
            mobile_phone_list.append('No phone')
    else:
        mobile_phone_list.append('No phone')


def get_names(response):
    names_list.append(response['first_name'])
    second_names_list.append(response['last_name'])


def get_city(response):
    if 'city' in response:
        cities_list.append(response['city']['title'])
    else:
        cities_list.append('No city')


def get_date(response):
    if 'bdate' in response:
        date_list.append(response['bdate'])
    else:
        date_list.append('No info')


def get_group_name(id_param):
    get_name = requests.get('https://api.vk.com/method/groups.getById', params={
            'access_token': tokens_list[1],
            'v': 5.131,
            'group_id': id_param,
            'fields': 'name'
        }).json()['response']
    return get_name[0]['name']


def append_group():
    group_id_list.append(group_id)


def get_union():
    logic_union_list.append('без логического объединения')


def get_offset(group_id):
    count = requests.get('https://api.vk.com/method/groups.getMembers', params={
            'access_token': tokens_list[1],
            'v': 5.131,
            'group_id': group_id,
            'sort': 'id_desc',
            'offset': 0,
            'fields': 'last_seen'
        }).json()['response']['count']
    return count / 1000


def get_users(group_id):
    type_of_group = ''
    if group_id.find('public') != -1:
        type_of_group = 'public'
        group_id = group_id[6:]
    elif group_id.find('club') != -1:
        type_of_group = 'club'
        group_id = group_id[4:]
    else:
        group_id = group_id
    offset = 0
    group_name = get_group_name(group_id)
    max_offset = get_offset(group_id)
    while offset <= max_offset:
        response = requests.post('https://api.vk.com/method/groups.getMembers', params={
            'access_token': tokens_list[1],
            'v': 5.131,
            'group_id': group_id,
            'sort': 'id_desc',
            'offset': offset * 1000,
            'lang': 'ru',
            'fields': 'contacts, city, bdate'})
        try:
            response = response.json()['response']
            new_group_id = type_of_group + group_id
            for item in response['items']:
                try:
                    good_id_list.append(str(item['id']))
                    group_id_list.append(new_group_id)
                    group_name_list.append(group_name)
                    get_city(item)
                    get_names(item)
                    get_phones(item)
                    get_date(item)
                except Exception as E:
                    continue
        except json.decoder.JSONDecodeError:
            print(response.status_code, response.content)
        offset += 1
    return good_id_list


if __name__ == '__main__':
    for filename in glob.glob(os.getcwd() + "\*.txt*"):
        with open(f"{filename}", "r") as file:
            group_ids = file.read().splitlines()
            new_filename = filename.split('\\')[6].split('.')[0]
        for group_id in group_ids:
            try:
                get_users(group_id.replace("https://vk.com/", ""))
            except KeyError as ke:
                time.sleep(1)
                print(f'{group_id}')
        for index, item in enumerate(mobile_phone_list):
            mobile_phone_list[index] = item.translate({ord(item): None for item in ' ()+-*....'})
            try:
                mobile_phone_list[index] = re.search(r'(8|7)9[0-9]{9}', item).group()
                if item[0] == '8':
                    mobile_phone_list[index] = '7' + item[1:11]
            except AttributeError:
                mobile_phone_list[index] = 'No phone'
    df = {'vk_id': good_id_list,
          'mobile_phone': mobile_phone_list,
          'name': names_list,
          'last_name': second_names_list,
          'city': cities_list,
          'birth_date': date_list,
          'group_id': group_id_list,
          'group_name': group_name_list}
    data = pd.DataFrame(df)
    result = data
    result.to_excel(os.getcwd() + f'//{new_filename}.xlsx', index=False)
