import requests
import unittest


API_KEY = '421d400bb146def70aef8fa0476c3d327294370210b04ca10a71f10d754b9da14fbf6a83455356abff5b6'
URL = 'https://api.vk.com/method/users.get'


class TestServerFunctionality(unittest.TestCase):
    def setUp(self):
        params = {
            'access_token': API_KEY,
            'user_id': '3967309',
            'v': 5.92,
        }
        self.response = requests.get(URL, params=params)

    def test_status(self):
        self.assertEqual(self.response.json()['response'][0]['id'], 3967309)

    def test_data(self):
        self.assertEqual(self.response.json()['response'][0]['first_name'], 'Ruslan')
        self.assertEqual(self.response.json()['response'][0]['last_name'], 'Ravilov')

    def tearDown(self):
        pass


if __name__ == '__main__':
    unittest.main()
