# -*- coding: utf-8 -*-
"""
Created on Wed Nov 22 09:06:57 2023

@author: Camilo
"""

#import requests
#import re
import sqlite3
from datetime import date
#from bs4 import BeautifulSoup
from priceScraper import get_price

#Create headers for the url request so the site does not recognize the scrapping attempt

headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Max-Age': '3600',
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'
    }

#Obtener las url de la tabla websites
hoy = date.today()
conexion = sqlite3.connect("monitoreo.db")
cursor = conexion.cursor()
websites = cursor.execute("SELECT nombre, sitio, url FROM websites")
precios = {}

#Obtener los precios de cada una de las paginas
for row in websites.fetchall():
    precios[row[0]] = (get_price(row[2], headers, row[1]))
    
for name, price in precios:
    cursor.execute("INSERT INTO precios (fecha, nombre, precio) VALUES (?, ?, ?", (hoy, name, price))
    
conexion.commit()
cursor.close()