from pymongo import MongoClient
from MongoDBAPI.models import TgUser
from FreelanceHabr.models import Task


class Mongod(MongoClient):

    db_name = 'FreelanceAgregator'
    tg_users_collection_name = 'TgBotUsers'
    habr_data_collection_name = 'HabrData'

    def __init__(self):
        super().__init__()

    def get_last_task(self, limit) -> None:
        if isinstance(limit, int):
            collection = self[Mongod.db_name][Mongod.habr_data_collection_name]
            return collection.find().sort('_id', -1).limit(limit)

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

    def add_user_to_db(self, user_data: TgUser) -> None:

        collection = self[Mongod.db_name][Mongod.tg_users_collection_name]

        json_to_db = {
            '_id': user_data.id,
            'tags': user_data.tags
        }

        return collection.insert_one(json_to_db)

    def get_current_state(self, user_id) -> None:
        collection = self[Mongod.db_name][Mongod.tg_users_collection_name]
        return collection.find_one({'_id': user_id})