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
    crit_dict = {'com_group': 0, 'com_bdate': 0, 'com_interests': 0}
    crit_dict['com_group'] = input('Введите вес для критерия - Общие группы (от 1 до 3): ')
    crit_dict['com_bdate'] = input('Введите вес для критерия - Возраст (от 1 до 3): ')
    crit_dict['com_interests'] = input('Введите вес для критерия - Интересы (от 1 до 3): ')

    return crit_dict

def main():
    get_auth = VKAuth(['friends'], '6889971', '5.95')
    get_auth.auth()
    print('Получен следующий токен {}'.format(get_auth._access_token))  # получили токен пользователя
    user_input = input('Введите id или имя пользователя: ')
    user_id = get_user_id(user_input, get_auth._access_token)
    user = User(get_auth._access_token, user_id)
    db = DB_Mongo()
    db.all_drop()
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
    max = input('Введите насколько лет партнер может быть старше ')
    min = input('Введите насколько лет партнер может быть младше ')
    db.put_value_bdate(partners_basic['user_data'][0]['bdate'], max, min)           # отметили в БД пользователей у которых общий
    # год рождения с User
    for part in partners_basic['user_data'][0]['interests'].split():    # отметили пересечение по общим интересам
        db.put_value_inter(part)
    db.print_basic_list()
    adv_criteries = adv_sort()
    db.find_n_drop_adv(adv_criteries)
    db.print_n_drop_db()


if __name__ == "__main__":
    main()

