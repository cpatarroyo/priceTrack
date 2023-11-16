# -*- coding: utf-8 -*-
"""
Created on Thu Nov  9 12:57:44 2023

@author: capat
"""

import requests
import re
import sqlite3
from datetime import date, timedelta
from bs4 import BeautifulSoup

###Scrape the data of interest from the website of interest
#Create headers for the url request so the site does not recognize the scrapping attempt
headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Max-Age': '3600',
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'
    }

read_url = "https://www.tiendasjumbo.co/nevera-haceb-311lt-brut-se-mi-tir2-gris-manj-inter/p"
read_url = "https://www.tiendasjumbo.co/harina-pan-blanca-x-1000-g/p"
read_url = "https://www.exito.com/nevera-no-frost-300-l-grafito-mabe-rma300fjcg-3037854/p"
read_url = "https://www.alkosto.com/nevera-no-frost-challenger-300-litros-cr317-titanium/p/7705191041766"
read_url = "https://www.homecenter.com.co/homecenter-co/product/71096/placa-de-yeso-st-1-2pg-122x244m-127mm-knauf/71096/"
read_url = "https://www.homecenter.com.co/homecenter-co/product/344300/bateria-auto-36ist600m/344300/"
req = requests.get(read_url,headers)

#HTML parsing to find the prices of the commodities reported (entry variables)
##Jumbo
priceSoup = BeautifulSoup(req.content, 'html.parser')
price = priceSoup.find('div', class_=['pr2'])
price.getText()

##Exito
priceSoup = BeautifulSoup(req.content, 'html.parser')
price = priceSoup.findAll('span', class_=['exito-vtex-components-4-x-currencyContainer'])

##alkosto
priceSoup = BeautifulSoup(req.content, 'html.parser')
price = priceSoup.find('span', id="js-original_price")

##homecenter
priceSoup = BeautifulSoup(req.content, 'html.parser')
price = priceSoup.findAll('span', class_='jsx-116178131')[1]


div.jsx-757574275:nth-child(2)
<span class="jsx-116178131">694.900</span>
for rem in [13,15,17]:
    del(priceInd[rem])

#HTML parsing to find the changes in the actionary market
read_url2 = "https://www.larepublica.co/indicadores-economicos/movimiento-accionario"
req2 = requests.get(read_url2,headers)
actionSoup = BeautifulSoup(req2.content, 'html.parser')
nameInd.extend(actionSoup.select('div.tableActions li a.nameAction'))
priceInd.extend(actionSoup.select('div.tableActions li span')[2:len(actionSoup.select('div.tableActions li span')):3])

results = {}

for i in range(len(nameInd)):
    results[nameInd[i].getText()] = re.sub(r'[,]','.',re.sub(r'[^0-9,]','',priceInd[i].getText()))

#HTML parsing to find the prices of the currencies (response variable)
read_url3 = "https://www.larepublica.co/indicadores-economicos/mercado-cambiario"
req3 = requests.get(read_url3,headers)
currencySoup = BeautifulSoup(req3.content, 'html.parser')
nameCur = currencySoup.select('h3.nameIndicator')
priceCur = currencySoup.select('span.priceIndicator')

curResults = {}

for j in range(len(nameCur)):
    curResults[nameCur[j].getText()] = re.sub(r'[,]','.',re.sub(r'[^0-9,]','',priceCur[j].getText()))

dbconnection = sqlite3.connect('cash.db')
cursor = dbconnection.cursor()
