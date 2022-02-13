import requests
from bs4 import BeautifulSoup
import pandas as pd
import csv
import json
import sys

header = {"User-Agent": 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:96.0) Gecko/20100101 Firefox/96.0'}

class Item(object):
    title = ""
    price = 0
    link = ""

    # The class "constructor" - It's actually an initializer
    def __init__(self, name, age, major):
        self.name = name
        self.age = age
        self.major = major

def requestWeb(url):
    page = requests.get(url, headers=header)
    soupe = BeautifulSoup(page.text, 'html.parser')
    return soupe

def search(name,website):
    if(website == "Ebay"):
        url = 'https://www.ebay.ca/sch/i.html?_from=R40&_nkw='+name+'&_sacat=0&rt=nc&_pgn=1'
    elif(website == "Stockx"):
        url = 'https://stockx.com/search?s='+name
    elif(website == "Kijiji"):
        url = 'https://www.kijiji.ca/b-ville-de-montreal/'+name+'/k0l1700281?rb=true&dc=true'
    soupe = requestWeb(url)
    return soupe

def scraper(name,website):
    soupe = search(name,website)
    products = []
    if(website == "Ebay"):
        results1 = soupe.find_all('div',{'class':'s-item__wrapper clearfix'})
        for item in results1:
            if(item.find('h3',{'class':'s-item__title'}).text != "Shop on eBay"):

                product1 = {
                    'title': item.find('h3',{'class':'s-item__title'}).text,
                    'price': item.find('span',{'class' : 's-item__price'}).text.replace('$','').replace('C',''),
                    'link': item.find('a',{'class': 's-item__link'})['href'],
                    # 'image': item.find('img',{'class':'s-item__image-img'})['src'],
                }
                products.append(product1)

    elif(website == "Stockx"):
        results2 = soupe.find_all("div",{"class":"css-1ibvugw-GridProductTileContainer"})
        for item in results2:
            product2 = {
                'title': item.find('p', {'class': 'chakra-text css-3lpefb'}).text,
                'price': item.find('p', {'class': 'chakra-text css-9ryi0c'}).text.replace('$','').replace('CA',''),
                'link': "https://stockx.com"+item.find('a')['href'],
                # 'image': item.find('div',{'class':'css-4tsjxp'}).text,
            }
            products.append(product2)
    elif(website == 'Kijiji'):
        results3 = soupe.find_all("div",{"class":"info"})
        for item in results3:
            product3 = {
                'title': item.find('div', {'class':"title"}).text.replace("\n","").replace('                            ',''),
                'price': item.find('div', {'class':"price"}).text.replace("\n","").replace("\xa0","").replace(" ","").replace('$','').replace('C',''),
                'link':  "https://www.kijiji.ca"+item.find('a',  {'class':"title"})['href'],
                 # 'img': item.find('img')['src'],
            }
            products.append(product3)
        results4 = soupe.find_all("div", {"class": "left-col"})
        # i=0
        # for item in results4:
        #     product3['img'].append(item.find('picture').text)
    return products

def run(name):
    products = []
    products += scraper(name,"Kijiji")
    products += scraper(name, "Ebay")
    products += scraper(name, "Stockx")

    productspd = pd.DataFrame(products)
    productspd.to_csv('output.csv', index=False)

    jsonArray = []
    with open('output.csv', encoding='utf-8') as csvf:
        #load csv file data using csv library's dictionary reader
        csvReader = csv.DictReader(csvf)

        #convert each csv row into python dict
        for row in csvReader:
            #add this python dict to json array
            jsonArray.append(row)

    with open('output.json', 'w', encoding='utf-8') as jsonf:
        jsonString = json.dumps(jsonArray, indent=4)
        jsonf.write(jsonString)

    print('CSV and JSON generated !')

    out_file = open('output.json','r+')
    out_file.write('{"item":[{')
    out_file.close();
    out_file = open('output.json', 'a+')
    out_file.write('}')
    out_file.close()
    return

productslist = run(sys.argv[0])