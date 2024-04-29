# -*- coding: utf-8 -*-
"""
Created on Thu Jul 27 09:43:26 2023

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

read_url = "https://www.larepublica.co/indicadores-economicos/commodities"
req = requests.get(read_url,headers)

#HTML parsing to find the prices of the commodities reported (entry variables)
indicatorSoup = BeautifulSoup(req.content, 'html.parser')
nameInd = indicatorSoup.findAll('h3', class_=['nameIndicator','col-10 pl-10 nameIndicator'])
priceInd = indicatorSoup.findAll(class_=['priceIndicator','price'])

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

### Table creation ###

#Command to create the prices table in the DB if it doesn't already exists
sqlcommand = """ CREATE TABLE IF NOT EXISTS prices (
id INT AUTO_INCREMENT PRIMARY KEY,
date VARCHAR NOT NULL,
name VARCHAR(50) NOT NULL,
price DOUBLE,
difference DOUBLE,
diff1w DOUBLE); """
cursor.execute(sqlcommand)

#Command to create the currency value table in the DB if it doesn't already exists
sqlcommand = """ CREATE TABLE IF NOT EXISTS currency (
cid INT AUTO_INCREMENT PRIMARY KEY,
date VARCHAR NOT NULL,
curname VARCHAR(10) NOT NULL,
price DOUBLE,
difference DOUBLE,
diff1w DOUBLE); """
cursor.execute(sqlcommand)

#Declare the variables for important days
today = date.today().strftime("%d/%m/%Y")
yesterday = date.today() - timedelta(1)
yesterday = yesterday.strftime("%d/%m/%Y")
weekago = date.today() - timedelta(5)
weekago = weekago.strftime("%d/%m/%Y")

#Select the highest id value to continue the autonumber process
cursor.execute('SELECT MAX(id) FROM prices')
counter = cursor.fetchone()[0]
#If there is no value for id (empty table), start from 0, or else start from the maximum id value +1
if counter is None:
    counter = 0
else:
    counter = counter + 1

#Select the highest id value for the currency table to continue the autonumber process
cursor.execute('SELECT MAX(cid) FROM currency')
curcounter = cursor.fetchone()[0]
#If there is no value for cid (empty table), start from 0, or else start from the maximum cid value +1
if curcounter is None:
    curcounter = 0
else:
    curcounter = curcounter + 1

#Query to fetch the name/price registries from yesterday and a week ago 
cursor.execute('SELECT name, price FROM prices WHERE date=?',(yesterday,))
listyester = dict(cursor.fetchall())
cursor.execute('SELECT name, price FROM prices WHERE date=?',(weekago,))
listweek = dict(cursor.fetchall())

for name in results:
    
    if name in listyester:
        yesterpr = float(((float(results[name])-float(listyester[name]))/float(results[name]))*100)
    else:
        yesterpr = None
    if name in listweek:
        weekpr = float(((float(results[name])-float(listweek[name]))/float(results[name]))*100)
    else:
        weekpr = None
    
    cursor.execute('INSERT INTO prices VALUES(?,?,?,?,?,?)',(counter,today,name,results[name],yesterpr,weekpr))
    counter = counter + 1

#Query to fetch the name/price pairs from yesterday and a week ago to compare the currencies
cursor.execute('SELECT curname, price FROM currency WHERE date=?',(yesterday,))
curyester = dict(cursor.fetchall())
cursor.execute('SELECT curname, price FROM currency WHERE date=?',(weekago,))
curweek = dict(cursor.fetchall())

for name in curResults:
    
    if name in curyester:
        yestercur = float(((float(curResults[name])-float(curyester[name]))/float(curResults[name]))*100)
    else:
        yestercur = None
    if name in curweek:
        weekcur = float(((float(curResults[name])-float(curweek[name]))/float(curResults[name]))*100)
    else:
        weekcur = None
    
    cursor.execute('INSERT INTO currency VALUES(?,?,?,?,?,?)',(curcounter,today,name,curResults[name],yestercur,weekcur))
    curcounter = curcounter + 1


dbconnection.commit()
dbconnection.close()
