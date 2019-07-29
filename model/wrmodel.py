import pandas as pd
import numpy as np
from collections import Counter

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



path = 'data/'


users = pd.read_json('rawdata/users.json',lines=True)



""" 이거 2월 22일 이후 아이템들, 작가에대한 각 아이템들 인기도임"""
js_d = open(path+'pop_writer_article.json').read() ; js_p = json.loads(js_d); 
pop_writer_article, new_article = js_p['pop_writer_article'] , js_p['new_article']



# test 정보

test = pd.read_csv('rawdata/predict/test.users',names=['id'])

test_list = test['id'].values.tolist()

# 본거 제거하기 위함

dataset2 = open(path + '/all_test_history.json',encoding='utf-8').read()
js2=json.loads(dataset2)
test_history = js2['all_test_history']


past_df2 = pd.read_csv(path + '18_read_raw.csv')

print('데이터 로드완료')


"""18일 이후에 최소 두번이상 본 작가"""

def author_(past_df, user_index):
    a = Counter(past_df[past_df.user_id.isin([user_index])].author).most_common()
    lim_twice_author = [x[0] for x in a if x[1] > 1]
    
    return lim_twice_author


print('추천시작')

"""fuck(두번이상 작가)에다가 한번이라도 본 팔로우 넣자, 그리고 중복제거"""
"""이 모델은 두번이상 작가와 그뒤에 히스토리중 한번이라도 본 팔로워를 붙인다음, 중복제거해서 번갈아 추천"""

def history_in_follow(past_df2,user_index):
    # a = 팔로우리스트
    # b = 히스토리작가(한번포함)
    # c = 팔로우중에 히스토리에 포함
    a =users[users.id.isin([user_index])].following_list.values[0]
    b =past_df2[past_df2.user_id.isin([user_index])].author.unique()
    c = [x for x in a if x in b]
    
    return c

#############################################
rec={}
for idx in tqdm(test_list):
    fuck =author_(past_df2, idx)
    
    #### users.json에 없는경우 그냥 패스
    try:
        fuck.extend(history_in_follow(past_df2,idx))
        fuck = list(OrderedDict(zip(fuck, repeat(None))))
    except IndexError:
        pass
    
    c=[]
    for i in range(1000):
        for j in fuck:
            try:
                c.append(pop_writer_article[j][i][0])
            except IndexError:
                pass
            
            except KeyError:# pop에 없는 작가가 들어오나보네?
                pass
    rec[idx] = c


######################################################

dev_dict = rec



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
fuck=[]
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

print('추천 중복제거 시작')

""" 브런치 리스트 빼고 실험"""

del_list =[]

for i in range(0,151):
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



predict_dict={}

for i in dev_dict:
    predict_dict[i] = dev_dict[i]

for i in tqdm(predict_dict):
    for j in del_list:
        if j in predict_dict[i]:
            predict_dict[i].remove(j)
##
final_predict={}

for i in dev_dict:
    final_predict[i] = predict_dict[i][:100]


print('추천 완료')

    
f= open('data/wr.txt','w')

rec1 =''
for i in tqdm(test_list):
    rec1+= '%s'%i
    if i in final_predict:
        pred = final_predict[i]
        for j in range(100):
            rec1 += ' %s'%pred[j]
        rec1 += '\n'
    
    else :
        for k in range(100):
            rec1 += ' %s' % itemlist3[k]
        
        rec1 += '\n'
        print('fuck')

f.write(rec1)
f.close()

print('저장 완료')



f= open('data/wr.txt')
line=f.readlines()
pd.DataFrame(line)[0].to_csv('data/wr_test.csv', index=False)


