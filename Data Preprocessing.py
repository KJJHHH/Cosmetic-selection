from itertools import groupby
import pandas as pd
import pickle
import numpy as np
import re

def get_productinfos(filename):
    with open(filename, "rb") as f:
        data_raw = pickle.load(f) 
    return data_raw

def tidy_data(data_raw):
    product_infos = pd.DataFrame()
    product_infos['productname_all'] = data_raw[0]
    product_infos['meanscore_all'] = data_raw[1]
    product_infos['brandname_all'] = data_raw[2]
    product_infos['color_all'] = data_raw[3]
    product_infos['price_all'] = data_raw[4]
    product_infos['capacity_all'] = data_raw[5]
    product_infos['tags_all'] = data_raw[6]
    product_infos['date_all'] = data_raw[7]
    return product_infos

def correct_data(product_infos):
    p = re.compile(r'\w\w\W\s\d\d\d')
    c = re.compile('\d\d\D\D')
    d = re.compile('\d\d\d\d\W\d\d\W\d\d')

    for k, i in enumerate(product_infos['price_all']): # price        
        if i != None:    
            # print(i)        
            a = p.findall(i)
            if a == [] and c.findall(i) != []:
                product_infos['price_all'][k] = None            
                product_infos['capacity_all'][k] = i
            if a == [] and d.findall(i) != []:
                product_infos['price_all'][k] = None 
                product_infos['date_all'][k] = i
    for k, i in enumerate(product_infos['capacity_all']): # capacity # different unit, mL, g       
        if i != None:    
            # print(i)        
            a = c.findall(i)
            #print('----------')
            #print(a)
            #print(i)
            if a == [] and p.findall(i) != []:        
                #print('x')   
                #print(i)     
                product_infos['capacity_all'][k] = None
                #print(product_infos['capacity_all'][k])            
                product_infos['price_all'][k] = i
            if a == [] and d.findall(i) != []:
                #print('y')
                #print(i)
                product_infos['capacity_all'][k] = None 
                # print(product_infos['capacity_all'][k])  
                product_infos['date_all'][k] = i
    for k, i in enumerate(product_infos['date_all']): # date      
        if i != None:    
            # print(i)        
            a = d.findall(i)            
            if a == [] and c.findall(i) != []:
                product_infos['date_all'][k] = None                      
                product_infos['capacity_all'][k] = i
            if a == [] and p.findall(i) != []:
                product_infos['date_all'][k] = None 
                product_infos['price_all'][k] = i

    product_infos = product_infos.dropna(axis = 0)
    return product_infos
                
# product_infos.index[product_infos['productname_all'] == '零粉感超持久粉底SPF38/PA+++']   

def get_potentialpriceproduct(max, min):
    
    goodproduct_name = []
    for i in product_infos['price_all'].groupby(product_infos['price_all']):
        price_str = i[0]
        price_num = float(i[0][4:])    
        
        if price_num<=max and price_num>=min:
            for k in product_infos[product_infos['price_all'] == i[0]].index.values:
                goodproduct_name.append(product_infos['productname_all'].loc[k])
    return goodproduct_name

def open_commentfile(goodproduct_name):
    comment_all = []
    for i in goodproduct_name:     
        try:        
            name = ("data/"+f"{i}.pickle".replace('/', ''))
            # print(name)
            with open(name, "rb") as f:
                comment_info = pickle.load(f)
            comment_all.append(comment_info)
        except:
            pass  
    return comment_all  

def get_skinagescore(comment_info):
    groupby(comment_info, lambda x: x == comment_info[0])
    comment_group = [list(group) for k, group in groupby(
        comment_info, lambda x: x == comment_info[0])]
    while True:
        try:
            comment_group.remove([comment_info[0]])
        except:
            break

    skintype_individual = []
    for i in comment_group:
        skintype_individual.append(i[0]) 

    score_individual = []
    for i in comment_group:
        score_individual.append(i[4][0])

    age_individual = []
    for i in comment_group:
        age_individual.append(float(i[1][:2]))

    return comment_info[0], skintype_individual, age_individual, score_individual

def getall_skinandscore(comment_all):
    skintype_all = []
    score_all = []
    productname_all = []
    age_all = []
    for comment_info in comment_all:       
        (productname, skintype_individual, age_individual,
            score_individual) = get_skinagescore(comment_info)           
        skintype_all.append(skintype_individual)
        score_all.append(score_individual) 
        age_all.append(age_individual)
        productname_all.append(productname)

    return productname_all, skintype_all, age_all, score_all

max = float(input('max'))
min = float(input('min'))
filename = "information.pickle"

data_raw = get_productinfos(filename)
product_infos = tidy_data(data_raw)
product_infos = correct_data(product_infos)  
goodproduct_name = get_potentialpriceproduct(max, min)
comment_all = open_commentfile(goodproduct_name)
(productname_all, skintype_all, age_all,
    score_all) = getall_skinandscore(comment_all)
prediction = pd.DataFrame()
prediction['productname'] = productname_all
prediction['skintype'] = skintype_all
prediction['age'] = age_all
prediction['score'] = score_all
    
#a = [123, 456]
#def abc():
#    a.append(234)
#    a[0] = 345
#    a = 543

#abc()
#print(a)
#with open("data/comment_allproduct[20].pickle", "rb") as f:
#    abc = pickle.load(f)
prediction

from sklearn import preprocessing
# Training
skinagenum = pd.DataFrame()
skin = []
age = []
score = []

le = preprocessing.LabelEncoder()
le.fit(['乾性肌膚', '普通性肌膚', '混合性肌膚', '油性肌膚', '敏感性肌膚', '先天過敏性肌膚'])

for i in range(len(prediction['skintype'][3])):
    skin_person = prediction['skintype'][3][i]
    age_person = prediction['age'][3][i]
    score_person = prediction['score'][3][i]
    skin.append(le.transform([skin_person]))
    age.append(age_person)
    score.append(score_person)


skinagenum['skin'] = skin
skinagenum['age'] = age
skinagenum['score'] = score
skinagenum
