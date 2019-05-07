from modules.vkauth import VKAuth
from modules.user import User


def main():
    get_auth = VKAuth(['friends'], '6889971', '5.95')
    get_auth.auth()
    print(get_auth._access_token)
    user = User(get_auth._access_token, get_auth._user_id)
    print(user.get_all_data())


if __name__ == "__main__":
    main()

