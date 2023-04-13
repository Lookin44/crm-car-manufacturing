import datetime
from typing import Dict

from django.utils.timezone import now


def facts_to_str(user_data: Dict[str, str]) -> str:
    facts = [f"{key} - {value}" for key, value in user_data.items()]
    return "\n".join(facts).join(["\n", "\n"])


def check_time() -> str:
    current_time = now().time()
    print(current_time)
    time_dict = {
        'Доброе утро': (datetime.time(6, 0), datetime.time(12, 0)),
        'Добрый день': (datetime.time(12, 0), datetime.time(18, 0)),
        'Добрый вечер': (datetime.time(18, 0), datetime.time(23, 59)),
        'Доброй ночи': (datetime.time(0, 0), datetime.time(6, 0))
    }
    for greeting, time_range in time_dict.items():
        if time_range[0] <= current_time <= time_range[1]:
            return greeting
