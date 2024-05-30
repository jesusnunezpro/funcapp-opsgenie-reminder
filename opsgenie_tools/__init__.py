import requests
import json
import logging
from datetime import datetime
from zoneinfo import ZoneInfo
from collections import namedtuple

Shift = namedtuple("Shift", "engineer type start end")

def convert_to_pacific(zdate:str) -> datetime:
    """
    Converts UTC in this format "2022-03-19T00:00:00Z" to Pacific Time datetime.
    Requires tzinfo from PyPI and Python 3.9
    """
    utc_datetime = datetime.strptime(zdate, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=ZoneInfo("UTC"))
    return utc_datetime.astimezone(ZoneInfo("US/Pacific"))


def get_shifts(schedule_name:str, weeks:int, api_key:str, test_data:str = "") -> list[namedtuple]:
    """
    Returns a list of Shift namedtuples.
    """
    if not test_data:
        url = f"https://api.opsgenie.com/v2/schedules/{schedule_name}/timeline?identifierType=name&interval={weeks}"
        headers = {
        'Authorization': f'GenieKey {api_key}'
        }

        response = requests.request("GET", url, headers=headers, data={})
        assert response.ok
        periods = response.json()["data"]["finalTimeline"]["rotations"][0]["periods"]
    else:
        periods = json.loads(test_data)["data"]["finalTimeline"]["rotations"][0]["periods"]
    shifts:list = []
    for period in periods:
        engineer = period["recipient"]["name"]
        shift_type = period["type"].title()
        start_dt = convert_to_pacific(period["startDate"])
        end_dt = convert_to_pacific(period["endDate"])
        shift = Shift(engineer, shift_type, start_dt.strftime('%c'), end_dt.strftime('%c'))
        logging.info(f"{shift=}")
        shifts.append(shift)
    return shifts

