from tqdm import tqdm_notebook
from tqdm import tqdm, trange
from collections import Counter
from datetime import timedelta, datetime
import glob
from itertools import chain
import json
import os
import re
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pandas.plotting import register_matplotlib_converters
import seaborn as sns
import matplotlib
import matplotlib.pyplot as plt
from collections import OrderedDict
from itertools import repeat
import time

print(' data loading')
#######
path = 'data/'


""" 이거 2월 22일 이후 아이템들, 작가에대한 각 아이템들 인기도임"""
js_d = open(path+'pop_writer_article.json').read() ; js_p = json.loads(js_d); 
pop_writer_article, new_article = js_p['pop_writer_article'] , js_p['new_article']


#######
users = pd.read_json('rawdata/users.json',lines=True)



# test 정보

test = pd.read_csv('rawdata/predict/test.users',names=['id'])
test_list = test['id'].values.tolist()


# 본거 제거하기 위함

dataset2 = open(path + '/all_test_history.json',encoding='utf-8').read()
js2=json.loads(dataset2)
test_history = js2['all_test_history']

print(' data load 완료')

"""57 test셋 만들기"""


users_follow=users[users.id.isin(pd.Series(test_list))]
users_follow = users_follow[['following_list','id']]
dev_dict={}
error={}

for i in users_follow.itertuples():
    dev_dict[i[2]] = i[1]
    
#dev_dict에는 팔로우한 작가의 글들이 인기순서대로 담기게됨   
for i in dev_dict:
    new=[]
    for j in dev_dict[i]:# 각 value의 list의 element에 접근
        try:
            new.extend(pop_writer_article[j])
        except KeyError:
            pass# 나중에 메타를 통해서 글로 바꾸는 작업 추가하기
        
    dev_dict[i] = new    

# 인기도 순으로 된 value값을 sort시키기
for i in dev_dict:
    dev_dict[i] = [x[0] for x in sorted(dev_dict[i], key= lambda element : element[1],reverse=True)]

# 이전에 구매했던 항목들 다없애기.
# dev_history에 유저의 정보가 없을 수 있음. (cold start user)
# pass 하면 굳이 if문으로 히스토리에서 제거할 필요없이, 그전 그대로 남게됨
for i in tqdm(dev_dict):
    try:
        dev_dict[i] = [x for x in dev_dict[i] if x not in test_history[i]]
    except KeyError:
        pass
    
#근데 아이템 리스트에 있는게 또 기존 히스토리랑 겹칠수도 있고, 기존에 인기추천했던거랑 겹칠수도 있음.
########################################################################################################
f = open('rawdata/0222_0301_1000_recommend.txt')
a =f.readline()
f.close()
itemlist3=a.replace(' ', ',').split(',')
del itemlist3[0]
itemlist3[-1] = itemlist3[-1][:-1]

    
########################################################################################################
# 기존 train history에도 없고, 기존에 추가해놨던 추천에도 없는 인기추천(1000)을 추가하겠음 뒷단에..
for i in tqdm(dev_dict):
    new=[]
    try:
        new.extend(dev_dict[i])
        #new.extend([x for x in itemlist3 if x not in test_history[i] and x not in dev_dict[i]])
        new.extend([x for x in itemlist3 if x not in dev_dict[i]])
        dev_dict[i] = new

    # cold start 93명인 경우는 그냥 기존에 추천했던거랑만 안겹치게
    except KeyError:
        new=[]
        new.extend(dev_dict[i])
        new.extend([x for x in itemlist3 if x not in dev_dict[i]])
        dev_dict[i] = new

print('추천 1완료')


print('중복 추천 삭제중')
del_list =[]

for i in range(150):
    del_list.append('@brunch_%s'%i)
    
for i in range(254):
    del_list.append('@dryjshin_%s'%i)
    
for i in range(6,28):
    del_list.append('@seochogirl_%s'%i)

for i in range(1646):
    del_list.append('@tenbody_%s'%i)
    
for i in range(313):
    del_list.append('@roysday_%s'%i)
    
for i in range(311):
    del_list.append('@yumileewyky_%s'%i)
    
for i in range(681):
    del_list.append('@varo_%s'%i)



for i in tqdm(dev_dict):
    for j in del_list:
        if j in dev_dict[i]:
            dev_dict[i].remove(j)

####

final_predict={}

for i in dev_dict:
    new=[]
    new.extend(dev_dict[i])
    new=new[:100]
    
    final_predict[i] = new

#####
print('중복 추천 삭제완료 추천완료')



f= open('data/follow.txt','w')

rec =''
for i in tqdm(test_list):
    rec+= '%s'%i
    if i in final_predict:
        pred = final_predict[i]
        for j in range(100):
            rec += ' %s'%pred[j]
        rec += '\n'
    
    else :
        itemlist4=itemlist3.copy()
        itemlist4=[x for x in itemlist4 if x not in test_history[i]]
        for k in range(100):
            rec += ' %s' % itemlist4[k]
        
        rec += '\n'
f.write(rec)
f.close()

print('follow model 예측파일 저장')



f= open('data/follow.txt')
line=f.readlines()
pd.DataFrame(line)[0].to_csv('data/follow_test.csv', index=False)
