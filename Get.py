from bs4 import BeautifulSoup
from selenium import webdriver
import requests
import os
#chrome driver
driver = webdriver.Chrome()


def get_url(search_term):
    #find the url based on search input
    template = 'https://www.amazon.com/s?k={}&crid=2P6HEO7U98X99&sprefix=ps5%2Caps%2C364&ref=nb_sb_noss_1'
    search_term = search_term.replace(' ','+')
    return template.format(search_term)
url = get_url('ps5 ')
driver.get(url)

#Extract the data using soup
soup = BeautifulSoup(driver.page_source,'html.parser')
results = soup.find_all('div',{'data-asin': True,'data-component-type':'s-search-result'})
item = results[0]
atag = item.h2.a
description = atag.text.strip()
url = 'https://www.amazon.com' + atag.get('href')


#generalize the pattern
def extract_record(item):
    #extract and return data from a single record

    #description and url
    atag = item.h2.a
    description = atag.text.strip() 
    url = 'https://www.amazon.com' + atag.get('href')
    try:
    #price
        
        price = item.find('span',class_='a-price-whole').text
        
    except AttributeError:
        return

    #rank and rating
    try:    
        rating = item.i.text
        review_count= item.find('span' , {'class':'a-size-base','dir':'auto'}).text
    except AttributeError:
        rating = ''
        review_count = ''
    #tuple for result
    result = (description,price,rating,review_count,url)
    
    return result

records = []
results = soup.find_all('div',{'data-component-type':'s-search-result'})
for item in results:
    record = extract_record(item)
    if record:
        records.append(record)
for row in records:
    print(row[1])


