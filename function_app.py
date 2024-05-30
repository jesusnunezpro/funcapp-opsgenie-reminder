import logging
import datetime
import os
import azure.functions as func
from pathlib import Path
from dotenv import load_dotenv

# This will test if the .env file exists and load it to the environment variables
if Path('.env').exists():
    load_dotenv()

# This environment variables will be used later
og_api_key = str(os.environ["og_api_key"])
og_schedule_url = str(os.environ["og_schedule_url"])
og_schedule_name = str(os.environ["og_schedule_name"])


# This is boilerplate code
app = func.FunctionApp()

@app.schedule(schedule="0 0 17 * * TUE", arg_name="myTimer", run_on_startup=True,
              use_monitor=False) 
def run_reminder(myTimer: func.TimerRequest) -> None:
    if myTimer.past_due:
        logging.info('The timer is past due!')

    logging.info('Python timer trigger function executed.')