import re
from pymongo import MongoClient


class DB_Mongo:
    def __init__(self):
        self.client = MongoClient('mongodb://localhost:27017/')
        self.db = self.client.hmwrk_db

    def import_data(self, dict_in):
        data = self.db.data
        data.insert_one(dict_in).inserted_id

    def drop(self):
        self.db.data.drop()

    def item_count(self):
        print(self.db.data.find().count())

    def find_n_drop_basic(self, criterian1, value1, criterian2, value2, criterian3, value3):

        # для каждого списка пользователей по базовому критерию
        # создается отдельная коллекция в Mongo DB

        find_buf_1 = self.db.buf
        find_buf_2 = self.db.buf2
        find_buf_3 = self.db.buf3

        # просеиваем результаты поиска согласно развесовке базовых критериев

        for item in self.db.data.find({criterian1: value1}):
            find_buf_1.insert_one(item).inserted_id
        for item in self.db.buf.find({criterian2: value2}):
            find_buf_2.insert_one(item).inserted_id
        for item in find_buf_2.find({criterian3: value3}):
            find_buf_3.insert_one(item).inserted_id

        for item in self.db.buf3.find():
            print(item)
        print('Найдено {} пользователей удовлетворяющих базовым критериям'.format(self.db.buf3.find().count()))

        # очищаем БД

        self.db.data.drop()
        self.db.buf.drop()
        self.db.buf2.drop()

    def find_n_drop_adv(self, criterian1, criterian2, criterian3):

        # для каждого списка пользователей по уточняющему критерию
        # создается отдельная коллекция в Mongo DB

        find_buf_3 = self.db.buf3
        find_buf_4 = self.db.buf4
        find_buf_5 = self.db.buf5
        find_buf_6 = self.db.buf6

        # просеиваем результаты поиска согласно развесовке базовых критериев

        for item in self.db.buf3.find({criterian1: 1}):
            find_buf_4.insert_one(item).inserted_id
        for item in self.db.buf4.find({criterian2: 1}):
            find_buf_5.insert_one(item).inserted_id
        for item in find_buf_5.find({criterian3: 1}):
            find_buf_6.insert_one(item).inserted_id
        print('Найдено {} пользователей удовлетворяющих уточняющим критериям'.format(self.db.buf6.find().count()))

        # очищаем БД

        self.db.buf3.drop()
        self.db.buf4.drop()
        self.db.buf5.drop()

    def put_fields(self):
        self.db.buf3.update({},
                          {'$set':{'com_group':0}},
                          multi=True)
        self.db.buf3.update({},
                            {'$set': {'com_bdate': 0}},
                            multi=True)
        self.db.buf3.update({},
                            {'$set': {'com_interests': 0}},
                            multi=True)

    def put_value_com(self, id_in):
        self.db.buf3.update({'id': id_in},
                            {'$set': {'com_group': 1}}, multi=True)


    def put_value_bdate(self, bdate_in):
        for item in self.db.buf3.find():
            if item.get('bdate') is not None:               # проверка на наличия поля bdate
                if item['bdate'][-4:] == bdate_in[-4:]:
                    self.db.buf3.update({'id': item['id']},
                                        {'$set': {'com_bdate': 1}}, multi=True)

    def put_value_inter(self, inter_in):
        regex = re.compile('.*' + inter_in + '.*')
        for item in self.db.buf3.find({'interests': regex}):
            self.db.buf3.update({'id': item['id']},
                                {'$set': {'com_interests': 1}}, multi=True)

    def get_basic_id(self):
        id_list = []
        for item in self.db.buf3.find():
            id_list.append(item['id'])
        return id_list

    def print_n_drop_db(self):
        for item in self.db.buf6.find():
            print(item)
        self.db.buf6.drop()



