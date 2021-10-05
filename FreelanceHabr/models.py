from dataclasses import dataclass, field
from typing import List


@dataclass
class Task:
    name: str = ''
    description: str = ''
    tags: List[str] = field(default_factory=list)
    url: str = ''
    price: str = ''
    views: str = ''
    responses: str = ''
    date: str = ''


@dataclass
class HabrTasks:
    tasks: List[Task] = field(default_factory=list)
