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
from priceScraper import get_price, get_dollar

#Create headers for the url request so the site does not recognize the scrapping attempt

#headers = {
#    'Access-Control-Allow-Origin': '*',
#    'Access-Control-Allow-Methods': 'GET',
#    'Access-Control-Allow-Headers': 'Content-Type',
#    'Access-Control-Max-Age': '3600',
#    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'
#    }

#Obtener las url de la tabla websites
hoy = date.today()
prdolar = get_dollar()
conexion = sqlite3.connect("monitoreo.db")
cursor = conexion.cursor()

#Crear la tabla de productos si es que no existe
prodCreateCommand = """ CREATE TABLE IF NOT EXISTS productos (
prodID INTEGER PRIMARY KEY AUTOINCREMENT,
nombre VARCHAR(50) NOT NULL,
tienda VARCHAR(20) NOT NULL,
url VARCHAR NOT NULL,
tipo VARCHAR); """
cursor.execute(prodCreateCommand)

#Crear la tabla de precios si es que no existe
precioCreateCommand = """ CREATE TABLE IF NOT EXISTS precios (
precioID INTEGER PRIMARY KEY AUTOINCREMENT,
prodID INT NOT NULL,
precio DOUBLE,
fecha DATE); """
cursor.execute(precioCreateCommand)

#Crear la tabla de monedas si es que no existe
monedaCreateCommand = """ CREATE TABLE IF NOT EXISTS monedas (
monID INTEGER PRIMARY KEY AUTOINCREMENT,
moneda VARCHAR(20),
precio DOUBLE NOT NULL,
fecha DATE); """
cursor.execute(monedaCreateCommand)

#Ingresar el precio del dolar del día
cursor.execute("INSERT INTO monedas (moneda, precio, fecha) VALUES (?, ?, ?)", ('Dolar',prdolar, hoy))

#Sacar los productos y las url de cada producto
websites = cursor.execute("SELECT prodID, url, tienda FROM productos")
precios = {}

#Obtener los precios de cada una de las paginas
for row in websites.fetchall():
    try:
        precios[row[0]] = (get_price(row[1], row[2], prdolar))
    except ValueError:
        print('Hay un valor erroneo!')
    
for prodId, precio in precios:
    cursor.execute("INSERT INTO precios (prodID, precio, fecha) VALUES (?, ?, ?)", (prodId, precio, hoy))
    
conexion.commit()
conexion.close()
