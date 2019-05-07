import time
import requests
import json


class User:
    def __init__(self, token, id):
        self.token = token
        self.id = id

    def get_all_data(self):
        params = {'access_token': self.token, 'v': 5.95,
                  'code': ''
                          'var usr_params = API.users.get({user_ids:' + str(self.id) + ', '
                          'fields: "sex, bdate, city, interests, relation"});'
                          'var people_lookfor = API.users.search({count: 10, city: (usr_params@.city)@.id[0], sex:(usr_params@.sex)[0]});'                                                             ''
                          'return {"people_lookfor": people_lookfor};'
                  }
        try:
            response = requests.get(
                'https://api.vk.com/method/execute',
                params
            )
            time.sleep(0.33)
            return response.json()
        except requests.exceptions.ConnectionError:
            print('Ошибка соединения. Ждем 5 сек после чего попытается восстановить связь!')
            time.sleep(5)
            try:
                response = requests.get(
                    'https://api.vk.com/method/execute',
                    params
                )
                time.sleep(0.33)
                return response.json()
            except requests.exceptions.ConnectionError:
                print('Ошибка соединения. Ждем 10 сек после чего попытается восстановить связь!')
                time.sleep(10)
                try:
                    response = requests.get(
                        'https://api.vk.com/method/execute',
                        params
                    )
                    time.sleep(0.33)
                    return response.json()
                except requests.exceptions.ConnectionError:
                    print('Ошибка соединения. Завершение работы Программы.')


