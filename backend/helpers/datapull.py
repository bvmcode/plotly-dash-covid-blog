
from datetime import datetime, timedelta
import logging
import pandas as pd

URL = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports_us/{}.csv'
FIELDS = ['Confirmed', 'Deaths', 'Recovered', 'Active']
START_DATE = datetime(2020,6,1)
FILE_PATH = './files/covid.csv'

def startup():
    logging.info('startup function - start')
    yesterday = datetime.now() + timedelta(days=-1)
    download_date = START_DATE
    header = False
    download = True

    while download:
        url_updated = URL.format(download_date.strftime('%m-%d-%Y'))
        logging.info(f'startup function - fetching url - {url_updated}')
        df = pd.read_csv(url_updated)
        df = df[df['Province_State'] == 'New Jersey'][FIELDS]
        df['date'] = download_date.strftime('%m-%d-%Y')
        if header == False:
            df.to_csv(FILE_PATH, index=False)
            header = True
        else:
            df.to_csv(FILE_PATH, mode='a', index=False, header=False)    
        download_date = download_date + timedelta(days=1)
        if download_date.date() > yesterday.date():
            download = False
    
    logging.info('startup function - end')

def nightly():
    logging.info('download_and_transform function - start')
    yesterday = datetime.now() + timedelta(days=-1)
    url_updated = URL.format(yesterday.strftime('%m-%d-%Y'))
    logging.info(f'download_and_transform function - fetching url - {url_updated}')
    df = pd.read_csv(url_updated)
    df = df[df['Province_State'] == 'New Jersey'][FIELDS]
    df['date'] = yesterday.strftime('%m-%d-%Y')
    df.to_csv(FILE_PATH, mode='a', header=False, index=False)
    logging.info('download_and_transform function - end')



