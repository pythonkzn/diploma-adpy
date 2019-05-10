import time
import requests
import json


class User:
    def __init__(self, token, id):
        self.token = token
        self.id = id

    def get_partners(self):
        params = {'access_token': self.token, 'v': 5.95,
                  'code': ''
                          'var usr_params = API.users.get({user_ids:' + str(self.id) + ', '
                          'fields: "sex, bdate, city, interests, relation"});'
                          'var city_list = API.users.search({count: 1000, '
                          'city: (usr_params@.city)@.id[0]});'  # получили список пользователей 
                                                                # с общим параметром city
                          'var sex_list = API.users.search({count: 1000, '
                          'sex: (usr_params@.sex)[0]});'  # получили список пользователей 
                                                          # с общим параметром sex
                          'var relation_list = API.users.search({count: 1000, status: (usr_params@.relation)[0]});' # получили список пользователей с общим параметром relation
                          'var partn_city_params = API.users.get({user_ids: city_list.items@.id, '
                          'fields: "sex, bdate, city, interests, relation"});'  # получили расширенную инфу
                                                                                # пользователей с общим параметром city
                          'var partn_sex_params = API.users.get({user_ids: sex_list.items@.id, '
                          'fields: "sex, bdate, city, interests, relation"});'  # получили расширенную инфу
                                                                                # пользователей с общим параметром sex               
                          'var partn_relation_params = API.users.get({user_ids: relation_list.items@.id, '
                          'fields: "sex, bdate, city, interests, relation"});'   # получили расширенную инфу
                                                                                 # пользователей с общим параметром 
                                                                                 # relation                                                        
                          'return {"partn_city": partn_city_params, "partn_sex": partn_sex_params,'
                          '"partn_relation": partn_relation_params, "user_data": usr_params};'
                  }
        try:
            response = requests.get(
                'https://api.vk.com/method/execute',
                params
            )
            time.sleep(0.33)
            return response.json()
            #['response']['people_list']['items']
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


