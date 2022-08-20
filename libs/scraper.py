#!/usr/bin/python3
# -*- coding:utf-8 -*-

import requests
from bs4 import BeautifulSoup

class ScrapingException(Exception):
    pass
        
class NoContractFound(ScrapingException):
    pass

class Scraper: 
    LOGIN_URL = "https://estateguru.co/portal/login/authenticate"
    
    def __init__(self, username, password):
        self.session = requests.session()
        self.username = username
        self.password = password
        self._connect()
        
    def _connect(self):
        """Connect to EG using login and password"""
        self.session.post(Scraper.LOGIN_URL, data={"username" : self.username, "password" : self.password}, headers=dict(referer=Scraper.LOGIN_URL))
        
    def _get_page(self, url):
        """download page"""
        return self.session.get(url).content
    
    def _get_table(self, page):
        """extract table from page"""
        soup = BeautifulSoup(page, 'lxml')
        table = soup.find('table')
        if not table:
            raise ScrapingException("Empty table")
        body = table.find('tbody')
        if not body:
            raise ScrapingException("Empty body")
        return body.find_all('tr')
    
    def _get_fields(self, row):
        """Gel list of fields from row"""
        return row.find_all('td')
    
    def _row_to_dict(self, row):
        """Convert raw data from row fields to pythonic data"""
        fields = self._get_fields(row)
        return {
        'name': DictBuilder.name(fields[1]),
        'id': DictBuilder.id(fields[2]),
        'type': DictBuilder.type(fields[3]),
        'country': DictBuilder.country(fields[4]),
        'state': DictBuilder.state(fields[5]),
        'sell price': DictBuilder.price(fields[6]),
        'buy price': DictBuilder.price(fields[7]),
        'remaining time': DictBuilder.time(fields[8]),
        'ROI': DictBuilder.roi(fields[9]),
        'selling date': DictBuilder.date(fields[10]),
        'url': DictBuilder.url(fields[3]),
        }
    
    def scrap(self, url):
        """Get page from URL, extract table and return a pythonic table"""
        page = self._get_page(url)
        table = self._get_table(page)
        try:
            return [self._row_to_dict(row) for row in table]
        except:
            raise NoContractFound
        
        
class DictBuilder:
    """Helper for converting raw data from table fields to pythonic data"""
    
    _COUNTRIES = {
    'ee': 'Estonia',
    'lv': 'Latvia',
    'de': 'Germany',
    'fi': 'Finland',
    'lt': 'Lithuania',
    'pt': 'Portugal',
    'se': 'Sweden',
    }
    
    @staticmethod
    def _remaining_time_to_days(remaining_time):
        """Get raw remaining time, convert it as days"""
        t, timeframe = remaining_time.split()
        if (timeframe == "months"):
            return int(t)*30
        elif (timeframe == "days"):
            return int(t)
    
    @staticmethod
    def name(name):
        if name:
            try:
                return name.find('img').attrs["alt"]
            except:
                return None
    
    @staticmethod
    def id(id):
        if id:
            try:
                return int(id.text.strip().replace('#', ''))
            except:
                return None
    
    @staticmethod
    def type(dtype):
        if dtype:
            try:
                return dtype.text.strip().split(' - ')[0]
            except:
                return None
    
    @staticmethod
    def country(country):
        if country:
            try:
                return DictBuilder._COUNTRIES[country.find('img').attrs['src'].split('/')[-1][0:2]]
            except:
                return None
        
    @staticmethod
    def state(state):
        if state:
            try:
                return state.text.strip()
            except:
                return None
    
    @staticmethod
    def price(price):
        if price:
            try:
                return float(price.text.strip().replace('€', '').replace(',', ''))
            except:
                return None
    
    @staticmethod
    def time(time):
        if time:
            try:
                return int(DictBuilder._remaining_time_to_days(time.text.strip()))
            except:
                return None
    
    @staticmethod
    def roi(roi):
        if roi:
            try:
                return float(roi.text.strip().replace('%', ''))
            except:
                return None
    
    @staticmethod
    def date(date):
        if date:
            try:
                return date.text.strip()
            except:
                return None
    
    @staticmethod
    def url(url):
        if url:
            try:
                return "https://estateguru.co" + url.find('a').attrs['href']
            except:
                return None
