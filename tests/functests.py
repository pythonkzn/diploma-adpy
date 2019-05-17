import unittest
import unittest
from modules.db_mongo import DB_Mongo


db = DB_Mongo()
dict_test = {'id': 4444444, 'first_name': 'Тест', 'last_name': 'Тестиков', 'is_closed': False,
             'can_access_closed': True, 'sex': 2, 'bdate': '3.9',
             'city': {'id': 60, 'title': 'Казань'}, 'relation': 6, 'interests': ''}

class TestFunc(unittest.TestCase):
    def test_import(self):
        db.import_data(dict_test)
        self.assertEqual(db.get_basic_id()[0], dict_test['id'])

    def test_drop(self):
        db.drop()
        self.assertEqual(db.item_count(), 0)


if __name__ == '__main__':
    unittest.main()