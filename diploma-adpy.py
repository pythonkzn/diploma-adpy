from modules.vkauth import VKAuth
from modules.user import User
from modules.db_mongo import DB_Mongo


def main():
    get_auth = VKAuth(['friends'], '6889971', '5.95')
    get_auth.auth()
    print(get_auth._access_token)
    user = User(get_auth._access_token, get_auth._user_id) # прошли авторизацию
    partners = user.get_partners()['response'] # получили три списка по одному общему критерию
    db = DB_Mongo()
    for item in partners['partn_city']:
        db.import_data(item)
    for item in partners['partn_sex']:
        db.import_data(item)
    for item in partners['partn_relation']:
        db.import_data(item)
    print(partners['user_data'])
    criterian_in_1 = 'relation'
    value_in_1 = partners['user_data'][0][criterian_in_1]
    criterian_in_2 = 'sex'
    value_in_2 = partners['user_data'][0][criterian_in_2]
    db.find_n_drop(criterian_in_1, value_in_1, criterian_in_2, value_in_2)


if __name__ == "__main__":
    main()

