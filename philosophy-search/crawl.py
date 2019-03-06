#coding:utf-8

import os
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

i = 0

def get_html(url):
    response = requests.get(url)
    response.encoding = 'utf-8'
    return response.text

def get_abstract(url):
    html= get_html(url)
    soup = BeautifulSoup(html,'lxml')
    try:
        abstract = soup.find('div',{'class':'intro'}).find('p').get_text().strip()
        return abstract
    except:
        return "  "

def get_book(html):
    soup = BeautifulSoup(html,'lxml')
    #获取每本书的div
    book_divs = soup.find_all('div',{'class':'info'})
    global i
    for book_div in book_divs:
        book_content = {}
        book_link = book_div.find('h2').find('a').get('href').strip()
        book_content['title'] = book_div.find('h2').find('a').get_text().strip()
        book_content['abstract'] = get_abstract(book_link)
        data = pd.DataFrame(book_content,index=[i])
        i += 1
        print(i)
        data.to_csv("book.csv",encoding='utf-8',mode='a',header=False)

    print ("to find next")
    next_link = soup.find('span',{'class':'next'}).find('a').get('href').strip()
    next_link = "https://book.douban.com"+ next_link
    print (next_link)
    html = get_html(next_link)
    print("next-link")
    time.sleep(1)
    if len(next_link) > 0:
        get_book(html)                  
    else:
        print ("end of crawl")

if __name__ == "__main__":
    url = "https://book.douban.com/tag/%E5%93%B2%E5%AD%A6?start=20&type=T"
    html = get_html(url)
    print (html)
    get_book(html)
