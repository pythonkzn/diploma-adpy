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


#    def find_by_name(name, db):
#        regex = re.compile('.*' + name + '.*')
#        concerts = db.concerts
#        for item in concerts.find({'Исполнитель': regex}).sort('Цена'):
#            print(item)


    def find_n_drop(self, criterian1, value1, criterian2, value2, criterian3, value3):

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

        for item in find_buf_3.find().limit(14):
            print(item)

        print('Найдено {} пользователей удовлетворяющих базовым критериям'.format(self.db.buf3.find().count()))

        # очищаем БД

        self.db.data.drop()
        self.db.buf.drop()
        self.db.buf2.drop()
        self.db.buf3.drop()


