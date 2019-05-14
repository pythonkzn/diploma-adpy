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


def adv_sort():
    # получаем развесовку уточняющих критериев через консоль

    crt_gr_in = input('Введите вес для критерия - Общие группы (от 1 до 3): ')
    crt_bdate_in = input('Введите вес для критерия - Возраст (от 1 до 3): ')
    crt_inter_in = input('Введите вес для критерия - Интересы (от 1 до 3): ')

    criterian_in_1 = ''
    criterian_in_2 = ''
    criterian_in_3 = ''
    value_in_1 = ''
    value_in_2 = ''
    value_in_3 = ''

    # распределяем развесовку введенную в консоли по переменным

    if crt_gr_in == '1':
        criterian_in_1 = 'com_group'
    elif crt_gr_in == '2':
        criterian_in_2 = 'com_group'
    elif crt_gr_in == '3':
        criterian_in_3 = 'com_group'

    if crt_bdate_in == '1':
        criterian_in_1 = 'com_bdate'
    elif crt_bdate_in == '2':
        criterian_in_2 = 'com_bdate'
    elif crt_bdate_in == '3':
        criterian_in_3 = 'com_bdate'

    if crt_inter_in == '1':
        criterian_in_1 = 'com_interests'
    elif crt_inter_in == '2':
        criterian_in_2 = 'com_interests'
    elif crt_inter_in == '3':
        criterian_in_3 = 'com_interests'

    criteries = [criterian_in_1, criterian_in_2, criterian_in_3]
    return criteries

def main():
    get_auth = VKAuth(['friends'], '6889971', '5.95')
    get_auth.auth()
    print('Получен следующий токен {}'.format(get_auth._access_token))  # получили токен пользователя
    user_input = input('Введите id или имя пользователя: ')
    user_id = get_user_id(user_input, get_auth._access_token)
    user = User(get_auth._access_token, user_id)
    db = DB_Mongo()
    partners_basic = user.get_partners_by_basic()['response']
    # получили cписок из тысячи человек отвечающих базовым критериям
    for item in partners_basic['fr_list']:
        db.import_data(item)
    print('Формируем список потенциальных друзей для {}'.format(partners_basic['user_data']))
    db.put_fields()  # создали поля для уточняющих критериев
    basic_id = db.get_basic_id()  # получили список id пользователей подходящих по базовым критериям
    i = 0
    for id in basic_id:
        print(i)
        if user.get_com_groups(user_id, id) > 1:  # отметили в БД пользователей у которых больше 1 общей группы с User
            db.put_value_com(id)
        i += 1

    db.put_value_bdate(partners_basic['user_data'][0]['bdate'])           # отметили в БД пользователей у которых общий
    # год рождения с User
    for part in partners_basic['user_data'][0]['interests'].split():    # отметили пересечение по общим интересам
        db.put_value_inter(part)
    adv_criteries = adv_sort()
    db.find_n_drop_adv(adv_criteries[0], adv_criteries[1], adv_criteries[2])
    db.print_n_drop_db()


if __name__ == "__main__":
    main()

