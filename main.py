from FreelanceHabr.FreelanceHabr import FreelanceHabr
from MongoDBAPI.MongoDBAPI import Mongod


def main():
    habr = FreelanceHabr()
    mongod = Mongod()

    tasks = habr.get_habr_tasks()
    last_five_tasks = mongod.get_last_task(5)
    for task in last_five_tasks:
        print(task['name'])


if __name__ == '__main__':
    main()
