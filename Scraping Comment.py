# Comment "review-content-container"

import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
import pickle

def get_pagelink():
    pagelink = []
    pagelink.append('https://www.cosme.net.tw/tags/105/ranking')
    for i in range(2,6):
        pagelink.append(
            f'https://www.cosme.net.tw/tags/105/ranking?skin=0&age=0&channel=0&effect=0&period=6&page={i}')
    return pagelink

def get_comment(productname): # a product

    product_commentall = []
    product_commentweird = []
    button = driver.find_elements(By.PARTIAL_LINK_TEXT, value = f"{productname}")       
    button[0].click()
    button = driver.find_elements(By.PARTIAL_LINK_TEXT, value='全部心得')
    button[0].click()
    for i in range(1000): # a page comment
        print(f'commentpage{i}')
        comment_rawinfo = driver.find_elements(By.CLASS_NAME, value = "review-content-container")

        for comment in comment_rawinfo: # a comment
            try:
                product_commentuseful = []
                comment_text = comment.text
                comment_split = comment_text.split('\n')
                skin = comment_split[1].split('・')[0]
                age = comment_split[1].split('・')[1]
                comment_ = comment_split[4]           
                (date, hit, score) = (comment_split[5], comment_split[6], comment_split[2])
            
                print('productname', productname)
                print('skin', skin)
                print('age', age)
                print('date', date)                
                print('hit', hit)
                print('score', score)
                print('comment', comment_)

                product_commentall.append(productname)
                product_commentall.append(skin)
                product_commentall.append(age)
                product_commentall.append(date)
                product_commentall.append(hit)
                product_commentall.append(score)
                product_commentall.append(comment_)
            except:
                product_commentweird.append(comment.text)

        product_commentall.append(product_commentuseful)
        try:
            button = driver.find_elements(By.PARTIAL_LINK_TEXT, value='下一頁')
            button[0].click()
        except:
            break
    
    return product_commentall, product_commentweird

def get_productname(product_links):
    productnames = []
    for productname in product_links:
        if productname.text != '':
            productnames.append(productname.text)
    return productnames

def get_commentinfoall(productnames, product_index):
    for productname in productnames:        
        print(productname)
        driver.get(f'{link}')
        comment_info, comment_info_weird = get_comment(productname)
        # globals()[f"{productname}"] = get_comment(productname)  
        # all_commentuseful.append(globals()[f'comment_allproduct[{productname}]'])
        # driver.back()        

        # print(globals()[str(productname)])
        with open("data/"+f"{productname}.pickle".replace('/', ''), "wb") as fi:
            pickle.dump(comment_info, fi)
        with open('data/weird/'+f'{productname}_weird.pickle'.replace('/', ''), 'wb') as fi:
            pickle.dump(comment_info_weird, fi)
        product_index+=1   
    return product_index
        

page_link = get_pagelink()

product_index = 0
for n, link in enumerate(page_link):
    n += 1
    print(f'--------------page {n}--------------')
    driver = webdriver.Chrome("C:/Users/USER/Desktop/chromedriver.exe")
    driver.get(f'{link}')
    product_links = driver.find_elements(By.CLASS_NAME, value = "uc-minor-link.single-dot")
    productnames = get_productname(product_links)
    product_index = get_commentinfoall(productnames, product_index)
