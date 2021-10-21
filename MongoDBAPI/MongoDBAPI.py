from pymongo import MongoClient
from FreelanceHabr.models import Task


class Mongod(MongoClient):

    db_name = 'FreelanceAgregator'
    tg_users_collection_name = 'TgBotUsers'
    habr_data_collection_name = 'HabrData'

    def __init__(self):
        super().__init__()

    def get_last_task(self, limit):
        if isinstance(limit, int):
            collection = self[Mongod.db_name][Mongod.habr_data_collection_name]
            tasks = collection.find().sort('_id', -1).limit(limit)
            result_list = []
            for task in tasks:
                result_list.append(task)
            return reversed(result_list)

    def find_task_in_db(self, task_id: Task.ID) -> None:
        if isinstance(task_id, str):
            collection = self[Mongod.db_name][Mongod.habr_data_collection_name]
            return collection.find_one({'_id': task_id})

    def add_habr_tasks_to_db(self, habr_data: Task) -> None:
        if isinstance(habr_data, Task):
            collection = self[Mongod.db_name][Mongod.habr_data_collection_name]

            json_to_db = {
                '_id': habr_data.ID,
                'site': habr_data.site,
                'name': habr_data.name,
                'description': habr_data.description,
                'tags': habr_data.tags,
                'url': habr_data.url,
                'price': habr_data.price,
                'views': habr_data.views,
                'responses': habr_data.responses,
                'date': habr_data.date
            }

            return collection.insert_one(json_to_db)
