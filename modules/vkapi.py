import requests

class VkApi:
    def __init__(self, token):
        self.token = token

    def get_user_id(self, usr_in):
        try:
            int(usr_in)
            return int(usr_in)
        except ValueError:
            params = {
                'user_ids': usr_in,
                'access_token': self.token,
                'v': 5.92,
                'fields': 'sex, bdate, city, interests, relation'
            }
            try:
                response_get_id = requests.get(
                    'https://api.vk.com/method/users.get',
                    params
                )
                return int(response_get_id.json()['response'][0]['id'])
            except Exception as e:
                print(response_get_id.json()['error']['error_msg'])

    def get_user_inf(self, id_in):
        params = {
            'user_ids': id_in,
            'access_token': self.token,
            'v': 5.92,
            'fields': 'sex, bdate, city, interests, relation'
        }
        try:
            response_get_usr = requests.get(
                'https://api.vk.com/method/users.get',
                params
            )
            return response_get_usr.json()
        except Exception as e:
            print(response_get_usr.json()['error']['error_msg'])