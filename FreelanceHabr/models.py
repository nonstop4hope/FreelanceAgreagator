from dataclasses import dataclass, field
from typing import List
import json


@dataclass
class Task:
    site: str = ''
    ID: str = ''
    name: str = ''
    description: str = ''
    tags: List[str] = field(default_factory=list)
    url: str = ''
    price: str = ''
    views: str = ''
    responses: str = ''
    date: str = ''

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, ensure_ascii=False, indent=4)




