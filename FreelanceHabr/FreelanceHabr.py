import requests
from bs4 import BeautifulSoup
from FreelanceHabr.models import Task
from urllib.parse import urljoin
from time import sleep
import random


class FreelanceHabr:

    def get_habr_task_description_and_date(self, url):
        description = ''
        date = ''
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            description = soup.find('div', class_='task__description').text.strip()
            date = soup.find('div', class_='task__meta').text.split(' • ')[0].strip()
            sleep(random.randint(2, 5))
            return description, date
        else:
            return description, date

    def get_habr_tasks(self, url: str = 'https://freelance.habr.com/tasks'):
        habr_tasks = []
        habr_response = requests.get(url)
        if habr_response.status_code == 200:
            soup = BeautifulSoup(habr_response.text, 'html.parser')

            tasks = soup.findAll('li', class_='content-list__item')

            for task in tasks:
                habr_task = Task()
                habr_task.site = 'habr.com'
                habr_task.ID = task.find('div', class_='task__title').find('a').get('href').split('/')[2]
                habr_task.name = task.find('div', class_='task__title').get('title')
                habr_task.url = urljoin(url, task.find('div', class_='task__title').find('a').get('href'))

                habr_task.views = task.find('span', class_='params__views icon_task_views').find('i').text
                habr_task.price = task.find('div', class_='task__price').text

                description, date = self.get_habr_task_description_and_date(habr_task.url)

                habr_task.description = description
                habr_task.date = date

                try:
                    habr_task.responses = task.find('span', class_='params__responses icon_task_responses'). \
                        find('i').text
                except AttributeError:
                    habr_task.responses = '0'

                tags_list = task.findAll('li', class_='tags__item')
                for tag in tags_list:
                    habr_task.tags.append(tag.find('a').text)

                habr_tasks.append(habr_task.to_json())

                break

        return habr_tasks







