import os
import opsgenie_tools
from dotenv import load_dotenv
from pathlib import Path

if Path('.env').exists():
    load_dotenv()

test_data = """
{
    "data": {
        "_parent": {
            "id": "12345678-ffff-1234-1234-ffff1b31ffff",
            "name": "Testing Schedule",
            "enabled": true
        },
        "startDate": "2022-03-21T07:00:00Z",
        "endDate": "2022-04-04T07:00:00Z",
        "finalTimeline": {
            "rotations": [
                {
                    "id": "12345678-ffff-1234-1234-ffff1b310887",
                    "name": "Product Name Goes Here",
                    "order": 1.0,
                    "periods": [
                        {
                            "startDate": "2022-03-26T00:00:00Z",
                            "endDate": "2022-03-28T00:00:00Z",
                            "type": "default",
                            "recipient": {
                                "id": "12345678-ffff-1234-1234-ffff1b311832",
                                "type": "user",
                                "name": "alice.lastname@example.com"
                            }
                        },
                        {
                            "startDate": "2022-04-02T00:00:00Z",
                            "endDate": "2022-04-04T00:00:00Z",
                            "type": "override",
                            "recipient": {
                                "id": "12345678-ffff-1234-1234-ffff1b3134fb",
                                "type": "user",
                                "name": "bob.familyname@example.com"
                            }
                        }
                    ]
                }
            ]
        }
    },
    "expandable": [
        "base",
        "forwarding",
        "override"
    ],
    "took": 0.144,
    "requestId": "12345678-ffff-1234-1234-ffff1b317aa3"
}
"""



og_api_key = str(os.environ["og_api_key"])
og_schedule_url = str(os.environ["og_schedule_url"])
og_schedule_name = str(os.environ["og_schedule_name"])

def test_convert_to_pacific_isPDT():
    pst_time = opsgenie_tools.convert_to_pacific("2022-03-21T07:00:00Z")
    assert pst_time.tzname() == 'PDT'

def test_convert_to_pacific_is_correct_isoformat():
    pst_time = opsgenie_tools.convert_to_pacific("2022-03-26T00:00:00Z")
    assert pst_time.isoformat() == '2022-03-25T17:00:00-07:00'

def test_get_shifts_firstengineer():
    shifts = opsgenie_tools.get_shifts(og_schedule_name, 2, og_api_key, test_data=test_data)
    assert shifts[0].engineer == "alice.lastname@example.com"

def test_get_shifts_override():
    shifts = opsgenie_tools.get_shifts(og_schedule_name, 2, og_api_key, test_data=test_data)
    assert shifts[1].type == "Override"

def test_get_shifts_returns2():
    shifts = opsgenie_tools.get_shifts(og_schedule_name, 2, og_api_key, test_data=test_data)
    assert len(shifts) == 2

# def test_send_email_notification():
#     dt_start = dt_end = opsgenie_tools.convert_to_pacific("2022-03-26T00:00:00Z")
#     test_shifts = [opsgenie_tools.Shift("jesus.nunez.pro@gmail.com", "Test",
#                                         dt_start.strftime('%c'), dt_end.strftime('%c')),
#                      ]
#     sent = opsgenie_tools.send_email_reminder(og_schedule_name, og_schedule_url, test_shifts, sg_api_key)
#     assert sent