# -*- coding: utf-8 -*-
"""
Created on Thu Nov  9 12:57:44 2023

@author: capat
"""

import requests
import re
from bs4 import BeautifulSoup
import json

def get_price(url, headers, website):
    req = requests.get(url,headers)
    priceSoup = BeautifulSoup(req.content, 'html.parser')
    if website == 'jumbo':
        price = priceSoup.find('div', class_=['pr2'])
    elif website == 'exito':
        jsonprice = json.loads(priceSoup.find('script', type='application/ld+json').getText())
        price = jsonprice['offers']['lowPrice']
    elif website == 'alkosto':
        price = priceSoup.find('span', id="js-original_price")
    elif website == 'homecenter':
        price = priceSoup.findAll('span', class_='jsx-116178131')[1]
    elif website == 'mercadolibre':
        jsonprice = json.loads(priceSoup.find('script', type='application/ld+json').getText())
        price = jsonprice['offers']['lowPrice']
    elif website == 'falabella':
        price = priceSoup.find('li', class_='jsx-329924046 prices-1')
        if price is None:
            price = priceSoup.find('li', class_='jsx-329924046 prices-0')
    return(float(re.sub(r'[,]','.',re.sub(r'[^0-9,]','',price.getText()))))
    

