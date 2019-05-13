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

def basic_sort(partners):
    # получаем развесовку базовых критериев через консоль

    crt_sex_in = input('Введите вес для критерия - Пол (от 1 до 3): ')
    crt_city_in = input('Введите вес для критерия - Город (от 1 до 3): ')
    crt_relation_in = input('Введите вес для критерия - Семейное положение (от 1 до 3): ')

    criterian_in_1 = ''
    criterian_in_2 = ''
    criterian_in_3 = ''
    value_in_1 = ''
    value_in_2 = ''
    value_in_3 = ''

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

    criteries = [criterian_in_1, value_in_1, criterian_in_2, value_in_2, criterian_in_3, value_in_3]
    return criteries


def main():
    get_auth = VKAuth(['friends'], '6889971', '5.95')
    get_auth.auth()
    print('Получен следующий токен {}'.format(get_auth._access_token))  # получили токен пользователя
    user_input = input('Введите id или имя пользователя: ')
    user_id = get_user_id(user_input, get_auth._access_token)
    user = User(get_auth._access_token, user_id)
    db = DB_Mongo()
    partners_basic = user.get_partners_by_basic()['response']     # получили три списка пользователей
                                                                  # по базовым критериям
    for item in partners_basic['partn_city']:
        db.import_data(item)
    for item in partners_basic['partn_sex']:
        db.import_data(item)
    for item in partners_basic['partn_relation']:
        db.import_data(item)
    print('Формируем список потенциальных друзей для {}'.format(partners_basic['user_data']))

    criteries = basic_sort(partners_basic)
    db.find_n_drop_basic(criteries[0], criteries[1], criteries[2], criteries[3], criteries[4], criteries[5])
    db.put_fields()  # создали поля для уточняющих критериев
    basic_id = db.get_basic_id()  # получили список id пользователей подходящих по базовым критериям
    for id in basic_id:
        if user.get_com_groups(user_id, id) > 1:  # отметили в БД пользователей у которых больше 1 общей группы с User
            db.put_value_com(id)

    db.put_value_bdate(partners_basic['user_data'][0]['bdate'])           # отметили в БД пользователей у которых общий
    # год рождения с User
    for part in partners_basic['user_data'][0]['interests'].split():    # отметили пересечение по общим интересам
        db.put_value_inter(part)
    db.print_n_drop_db()

if __name__ == "__main__":
    main()

