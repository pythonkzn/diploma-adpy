from modules.vkauth import VKAuth
from modules.vkexec import VkExecute
from modules.db_mongo import DB_Mongo
from modules.vkapi import VkApi


def adv_sort():
    # получаем развесовку уточняющих критериев через консоль
    crit_dict = {'com_group': 0, 'com_bdate': 0, 'com_interests': 0}
    crit_dict['com_group'] = input('Введите вес для критерия - Общие группы (от 1 до 3): ')
    crit_dict['com_bdate'] = input('Введите вес для критерия - Возраст (от 1 до 3): ')
    crit_dict['com_interests'] = input('Введите вес для критерия - Интересы (от 1 до 3): ')
    return crit_dict


def get_basic_partners(user_in, user_full_in):
    usr_full_var = user_full_in['response'][0]
    if 'city' not in user_full_in['response'][0]:
        usr_full_var['city'] = {'id': 0, 'title': ''}
        usr_full_var['city']['id'] = input('Введите код города по которому нужно проводить поиск: ')
    if 'bdate' not in user_full_in['response'][0]:
        usr_full_var['bdate'] = ''
        usr_full_var['bdate'] = input('Введите дату рождения в формате "D.M.YYYY": ')
    if len(user_full_in['response'][0]['bdate']) < 6:
        usr_full_var['bdate'] = ''
        usr_full_var['bdate'] = input('Введите дату рождения в формате "D.M.YYYY": ')
    partners_basic_out = user_in.get_partners_by_basic(usr_full_var['sex'], usr_full_var['city']['id'])['response']
    return partners_basic_out


def db_operation(db_in, partners_basic_in, user_full_in, user_in, user_id_in):
    for item in partners_basic_in['fr_list']:
        db_in.import_data(item)
    print('Формируем список потенциальных друзей для {}'.format(user_full_in['response']))
    db_in.put_fields()  # создали поля для уточняющих критериев
    basic_id = db_in.get_basic_id()  # получили список id пользователей подходящих по базовым критериям
    i = 0
    for id in basic_id:
        print('Обработка {} записи из {}'.format(i,len(basic_id)))
        if user_in.get_com_groups(user_id_in, id) > 1:  # отметили в БД пользователей у которых больше 1 группы с User
            db_in.put_value_com(id)
        i += 1
    max = input('Введите насколько лет партнер может быть старше ')
    min = input('Введите насколько лет партнер может быть младше ')
    db_in.put_value_bdate(user_full_in['response'][0]['bdate'], max, min)  # отметили в БД пользователей у которых общий
    # год рождения с Userъ
    if 'interests' in user_full_in['response'][0].keys():
        for part in user_full_in['response'][0]['interests'].split():    # отметили пересечение по общим интересам
            db_in.put_value_inter(part)


def main():
    get_auth = VKAuth(['friends'], '6889971', '5.95')
    get_auth.auth()
    print('Получен следующий токен {}'.format(get_auth._access_token))  # получили токен пользователя
    user_input = input('Введите id или имя пользователя: ')
    vkapi = VkApi(get_auth._access_token)
    user_id = vkapi.get_user_id(user_input)
    user_full = vkapi.get_user_inf(user_id)
    user = VkExecute(get_auth._access_token, user_id)
    db = DB_Mongo()
    db.all_drop()
    partners_basic = get_basic_partners(user, user_full)    # получили cписок из 200 человек по базовым критериям
    db_operation(db, partners_basic, user_full, user, user_id)    # записали базовый список в БД
    adv_criteries = adv_sort()    # сформировали уточняющие критерии
    db.find_n_drop_adv(adv_criteries)    # отсортировали по уточняющим критериям
    db.print_n_drop_db()


if __name__ == "__main__":
    main()

