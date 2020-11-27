import os
import logging
from datetime import datetime
from apscheduler.schedulers.blocking import BlockingScheduler
from helpers.datapull import download_and_transform, startup

os.environ['TZ']= 'America/Chicago'
method = os.environ['METHOD']

def get_data():
    if method == 'startup':
        startup()
        return
    download_and_transform()

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, filename="./logs/main.log", format='%(asctime)s:%(levelname)s:%(message)s')
    scheduler = BlockingScheduler()
    scheduler.add_job(get_data, 'cron', minute='58', hour='06', day='*', year='*', month='*')
    scheduler.start()
