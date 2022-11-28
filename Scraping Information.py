import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
import pickle

# driver = webdriver.Chrome("C:/Users/USER/Desktop/chromedriver.exe")
# driver.get('https://www.cosme.net.tw/tags/105/ranking?skin=0&age=0&channel=0&effect=0&period=6&page=2')
# link product name
# product_links = driver.find_elements(By.CLASS_NAME, value = "uc-minor-link.single-dot")
# get each product detail
# info
def get_pagelink():
    pagelink = []
    pagelink.append('https://www.cosme.net.tw/tags/105/ranking')
    for i in range(2,6):
        pagelink.append(
            f'https://www.cosme.net.tw/tags/105/ranking?skin=0&age=0&channel=0&effect=0&period=6&page={i}')
    return pagelink

def get_productinfo():
    # meanscore
    try:
        meanscore = driver.find_elements(By.CLASS_NAME, value = "score-number")[0].text
        print('meanscore:', meanscore)
    except:
        meanscore = None
        print('meanscore:', None)

    # brandname <a class="uc-main-link" href="/brands/113">YSL 聖羅蘭</a>
    try:
        brandname = driver.find_elements(By.CLASS_NAME, value = "uc-main-link")[0].text
        print('brandname:', brandname)
    except:
        brandname = None
        print('brandname:', None)

    # color
    # //*[@id="uc-product-detail-content"]/div[2]/div/div/div[1]/div[2]/div
    # //*[@id="uc-product-detail-content"]/div[2]/div/div/div[2]/div[2]/div
    try:
        colors = []
        button = driver.find_elements(
                By.CLASS_NAME, 
                value = 'details-container-toggle-text.uc-main-link')
        button[0].click()
        for i in range(10000):
            k=i+1
            color = driver.find_elements(
                By.XPATH, 
                value = f'//*[@id="uc-product-detail-content"]/div[2]/div/div/div[{k}]/div[2]/div')
            if color == []:
                break
            colors.append(color[0].text)
        print('colors:', colors)
    except:
        colors = None
        print('colors:', None)

    # capacity <div class="other-text">25ml</div>
    try:
        capacity = driver.find_elements(By.CLASS_NAME, value = "other-text")[0].text
        print('capacity:', capacity)
    except:
        capacity = None
        print('capacity:', None)                

    # price <div class="other-text">NT$ 2600</div>
    try:
        price = driver.find_elements(By.CLASS_NAME, value = "other-text")[1].text
        print('price:', price)
    except:
        price = None
        print('price:', None)

    # tags 
    # /html/body/div[2]/div[3]/div[1]/div[7]/div[2]/div[5]/div[2]/a[13]
    # /html/body/div[2]/div[3]/div[1]/div[7]/div[2]/div[5]/div[2]/a[12]
    try:
            tags = []
            for i in range(10000):
                k=i+1
                tag = driver.find_elements(
                    By.XPATH, 
                    value = f'/html/body/div[2]/div[3]/div[1]/div[7]/div[2]/div[5]/div[2]/a[{k}]')
                if tag == []:
                    break
                tags.append(tag[0].text)
            print('tags:', tags)
    except:
            tags = None
            print('tags:', None)

    # date <div class="other-text">2022.07.01</div>
    try:
            date = driver.find_elements(By.CLASS_NAME, value = "other-text")[2].text
            print('date:', date)
    except:
            date = None
            print('date:', None)

    driver.back()
    return (meanscore, brandname, colors, price, capacity, tags, date)

products_details = pd.DataFrame()
productname_all = []
meanscore_all = []
brandname_all = []
color_all = []
price_all = []
capacity_all = []
tags_all = []
date_all = []
comments = pd.DataFrame()

page_link = get_pagelink()

for n, link in enumerate(page_link):
    n += 1
    print(f'--------------page {n}--------------')
    driver = webdriver.Chrome("C:/Users/USER/Desktop/chromedriver.exe")
    driver.get(f'{link}')
    product_links = driver.find_elements(By.CLASS_NAME, value = "uc-minor-link.single-dot")
    productnames = []
    for productname in product_links:
        if productname.text != '':
            productnames.append(productname.text)

    
    for productname in productnames:
        print('product name:', productname)
        button = driver.find_elements(By.PARTIAL_LINK_TEXT, value = f"{productname}")
        print(button)
        button[0].click()
        (meanscore, brandname, colors, price, capacity, 
        tags, date) = get_productinfo()            

        productname_all.append(productname)
        meanscore_all.append(meanscore)
        brandname_all.append(brandname)
        color_all.append(colors)
        price_all.append(price)
        capacity_all.append(capacity)
        tags_all.append(tags)
        date_all.append(date)

products_detaillist = []
products_detaillist.append(productname_all)
products_detaillist.append(meanscore_all)
products_detaillist.append(brandname_all)
products_detaillist.append(color_all)
products_detaillist.append(price_all)
products_detaillist.append(capacity_all)
products_detaillist.append(tags_all)
products_detaillist.append(date_all)
