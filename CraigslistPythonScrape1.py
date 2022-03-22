#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 18 01:10:09 2022

@author: kevinvu
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import seaborn as sns
URL="https://sfbay.craigslist.org/search/apa?min_bedrooms=1&minSqft=1&availabilityMode=0&sale_date=all+dates"

page=requests.get(URL)

soup=BeautifulSoup(page.content, "html.parser")
results=soup.find(class_="rows")


rental_element=results.find_all('li', class_="result-row")
title = []; rent =[]; br=[]; sqft=[]
for rental_elem in rental_element:
    rent_elem=rental_elem.find('span', class_='result-price')
    title_elem=rental_elem.find('h3', class_='result-heading')
    if rental_elem.find('span', class_='housing') is not None:
        if 'ft2' in rental_elem.find('span', class_='housing').text.split()[0]:
            br_elem=np.nan
            sqft_elem=int(rental_elem.find('span', class_ = 'housing').text.replace('ft2',"").split()[0])
        elif len(rental_elem.find('span', class_='housing').text.split())>2:
            br_elem=int(rental_elem.find('span', class_='housing').text.replace('br',"").split()[0])
            sqft_elem=int(rental_elem.find('span', class_ = 'housing').text.replace('ft2',"").split()[2])
        elif len(rental_elem.find('span', class_='housing').text.split())==2:
            br_elem=int(rental_elem.find('span', class_='housing').text.replace('br',"").split()[0])
            br.append(br_elem)
            sqft_elem=np.nan
        else:
            br_elem=np.nan
            sqft_elem=np.nan
          
    title.append(title_elem.text.strip())
    rent.append(int(rent_elem.text.strip("$").replace(",","")))
    sqft.append(sqft_elem)
    br.append(br_elem)
    
data = list(zip(title,rent,br,sqft))

df = pd.DataFrame(data,columns=["Listing","Monthly Rent","Bedroom Count","SqFt"])

sns.scatterplot(data=df,x="Monthly Rent", y="SqFt",hue="Bedroom Count", palette="crest", s=70).set(title="SF/Bay Area Craigslist Rent x Square Footage")



