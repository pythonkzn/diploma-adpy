from modules.vkauth import VKAuth
from modules.user import User
from modules.db_mongo import DB_Mongo
import requests


def get_user_id(usr_in, token):
    try:
        int(usr_in)
        return int(usr_in)
    except ValueError:
        params = {
            'user_ids': usr_in,
            'access_token': token,
            'v': 5.92
        }
        try:
            response_get_id = requests.get(
                'https://api.vk.com/method/users.get',
                params
            )
            id = int(response_get_id.json()['response'][0]['id'])  # получили по имени пользователя его id
            return id
        except Exception as e:
            print(response_get_id.json()['error']['error_msg'])


def main():
    get_auth = VKAuth(['friends'], '6889971', '5.95')
    get_auth.auth()
    print('Получен следующий токен {}'.format(get_auth._access_token))
    user_input = input('Введите id или имя пользователя: ')
    user_id = get_user_id(user_input, get_auth._access_token)
    user = User(get_auth._access_token, user_id)
    partners = user.get_partners_by_basic()['response'] # получили три списка пользователей
                                                        # по базовым критериям
    db = DB_Mongo()
    for item in partners['partn_city']:
        db.import_data(item)
    for item in partners['partn_sex']:
        db.import_data(item)
    for item in partners['partn_relation']:
        db.import_data(item)
    print('Формируем список потенциальных друзей для {}'.format(partners['user_data']))

    # получаем развесовку базовых критериев через консоль

    crt_sex_in = input('Введите вес для критерия - Пол (от 1 до 3): ')
    crt_city_in = input('Введите вес для критерия - Город (от 1 до 3): ')
    crt_relation_in = input('Введите вес для критерия - Семейное положение (от 1 до 3): ')

    # распределяем развесовку введенную в консоли по переменным

    if crt_sex_in == '1':
        criterian_in_1 = 'sex'
        value_in_1 = partners['user_data'][0][criterian_in_1]
    elif crt_sex_in == '2':
        criterian_in_2 = 'sex'
        value_in_2 = partners['user_data'][0][criterian_in_2]
    elif crt_sex_in == '3':
        criterian_in_3 = 'sex'
        value_in_3 = partners['user_data'][0][criterian_in_3]

    if crt_city_in == '1':
        criterian_in_1 = 'city'
        value_in_1 = partners['user_data'][0][criterian_in_1]
    elif crt_city_in == '2':
        criterian_in_2 = 'city'
        value_in_2 = partners['user_data'][0][criterian_in_2]
    elif crt_city_in == '3':
        criterian_in_3 = 'city'
        value_in_3 = partners['user_data'][0][criterian_in_3]

    if crt_relation_in == '1':
        criterian_in_1 = 'relation'
        value_in_1 = partners['user_data'][0][criterian_in_1]
    elif crt_relation_in == '2':
        criterian_in_2 = 'relation'
        value_in_2 = partners['user_data'][0][criterian_in_2]
    elif crt_relation_in == '3':
        criterian_in_3 = 'relation'
        value_in_3 = partners['user_data'][0][criterian_in_3]

    db.find_n_drop(criterian_in_1, value_in_1, criterian_in_2, value_in_2, criterian_in_3, value_in_3)


if __name__ == "__main__":
    main()

