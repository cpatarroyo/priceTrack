# -*- coding: utf-8 -*-
"""
Created on Thu Nov  9 12:57:44 2023

@author: capat
"""

import requests
import re
from bs4 import BeautifulSoup
import json

def get_price(url, website, prdolar):
    req = requests.get(url)
    priceSoup = BeautifulSoup(req.content, 'html.parser')
    if website == 'jumbo':
        price = priceSoup.find('div', class_=['pr2'])
    elif website == 'exito':
        jsonprice = json.loads(priceSoup.find('script', type='application/json').getText())
        price = jsonprice['props']['pageProps']['data']['product']['sellers'][0]['commertialOffer']['Price']
    elif website == 'alkosto':
        price = priceSoup.find('span', id="js-original_price")
    elif website == 'homecenter':
        price = priceSoup.findAll('span', class_='jsx-116178131')[1]
    elif website == 'mercadolibre':
        jsonprice = json.loads(priceSoup.find('script', type='application/ld+json').getText())
        price = jsonprice['offers']['price']
    elif website == 'falabella':
        price = priceSoup.find('li', class_='jsx-329924046 prices-1')
        if price is None:
            price = priceSoup.find('li', class_='jsx-329924046 prices-0')
    elif website == 'drogueria_colsubsidio':
        scripts = priceSoup.findAll('script')
        matchscript = [x for x in scripts if 'productPriceTo' in x.getText()]
        tempdict = json.loads(matchscript[0].getText()[matchscript[0].getText().index('(')+1:matchscript[0].getText().index(')')])
        price = float(tempdict['productPriceTo'])
    elif website == 'olimpica':
        price = priceSoup.find('meta', property='product:price:amount')
        price = float(price['content'])
    elif website == 'drogueria_cafam':
        price = priceSoup.find('span', itemprop='price')
        price = float(price['content'])
    elif website == 'drogas_la_rebaja':
        temprice = priceSoup.findAll('script')
        matchscript = [x for x in temprice if 'lowPrice' in x.getText()]
        tempdict = json.loads(matchscript[0].getText())
        matchdict = [y for y in tempdict.keys() if 'listPrice' in y]
        price = tempdict[matchdict[0]]['lowPrice']
    elif website == 'farmatodo':
        price = priceSoup.find('p',class_='p-blue')
    elif website == 'locatel':
        price = priceSoup.find('span', class_='vtex-store-components-3-x-currencyContainer vtex-store-components-3-x-currencyContainer--contentPricePdp')
    elif website == 'amazon':
        temprice = priceSoup.find('span', class_ = 'a-price')
        if temprice is None:
            price = None
        else:
            temprice = temprice.getText().split('$')[1]
            price = prdolar * float(re.sub(r'[,]','.',re.sub(r'[^0-9.,]','',temprice)))
    
    if isinstance(price,(int,float)):
        return(float(price))
    elif price is None:
        return(price)
    else:
        return(float(re.sub(r'[,]','.',re.sub(r'[^0-9,]','',price.getText()))))
    
def get_dollar():
    DOLLARURL = 'https://www.larepublica.co/indicadores-economicos/mercado-cambiario/dolar'
    req = requests.get(DOLLARURL)
    dolSoup = BeautifulSoup(req.content, 'html.parser')
    dollar = dolSoup.find('span',class_='price')
    return(float(re.sub(r'[,]','.',re.sub(r'[^0-9,]','',dollar.getText()))))
