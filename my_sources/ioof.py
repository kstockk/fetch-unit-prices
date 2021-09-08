
"""Fetch unit prices from IOOF's website
"""

from datetime import datetime
from dateutil import tz
from dateutil.parser import parse
import requests
import json
from bs4 import BeautifulSoup

from beancount.prices import source
from beancount.core.number import D

"""
bean-price -e 'AUD:my_sources.ioof/IOF0097AU'
"""

BASE_URL = 'https://www.ioof.com.au/performance/unit-prices'
CURRENCY = 'AUD'

class Source(source.Source):

    def get_url(self, ticker):
        try:
            page = requests.get(BASE_URL)
            soup = BeautifulSoup(page.content, 'html.parser')
            table = soup.find(class_='table table-striped')
            rows = table.find_all('tr')[1:]

            for row in rows:
                r = {}
                cols = row.find_all('td')
                if cols[1].text.strip() == ticker:
                    url = cols[0].a['href']
            return url
        except:
            raise ValueError('Invalid ticker')

    def get_latest_price(self, ticker):
        try:
            url = self.get_url(ticker)
            page = requests.get('https://www.ioof.com.au/' + url)
            soup = BeautifulSoup(page.content, 'html.parser')
            table = soup.find(class_='table table-striped unit-price-details')
            row = table.find_all('tr')[1]

            col = row.find_all('td')
            eff_date = parse(col[0].text.strip()).strftime('%Y-%m-%d')
            time = datetime.strptime(eff_date, '%Y-%m-%d').replace(tzinfo=tz.tzutc())
            price = D(col[2].text.strip())
            return source.SourcePrice(price, time, CURRENCY)
        except UnboundLocalError:
            return None
        except AttributeError:
            return None

    def get_historical_price(self, ticker, time):
        try:
            url = self.get_url(ticker)
            page = requests.get('https://www.ioof.com.au/' + url)
            soup = BeautifulSoup(page.content, 'html.parser')
            table = soup.find(iclass_='table table-striped unit-price-details')
            rows = table.find_all('tr')[1:]

            date = time.strftime('%Y-%m-%d')
            for row in rows:
                cols = row.find_all('td')
                eff_date = parse(cols[0].text.strip()).strftime('%Y-%m-%d')
                if eff_date == date:
                    price = D(cols[2].text.strip())
            return source.SourcePrice(price, time, CURRENCY)
        except UnboundLocalError:
            return None
        except AttributeError:
            return None
