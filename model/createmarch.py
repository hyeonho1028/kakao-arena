#!/usr/bin/env python
# coding: utf-8

# In[1]:


import random
import time
from collections import Counter
from datetime import timedelta, datetime
import glob
from itertools import chain
import json
import datetime
import os
import re
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def seed_everything(seed):
    random.seed(seed)
    os.environ['PYTHONHASHSEED'] = str(seed)
    np.random.seed(seed)
#     torch.manual_seed(seed)
#     torch.cuda.manual_seed(seed)
#     torch.backends.cudnn.deterministic = True

SEED = 42
seed_everything(SEED)

N_FOLDS = 5


# # data load

# In[2]:


path = 'data/'

read = pd.read_csv(path + 'read.csv')
from itertools import chain
def chainer(s):
    return list(chain.from_iterable(s.str.split(' ')))
read_cnt_by_user = read['article_id'].str.split(' ').map(len)
read_raw = pd.DataFrame({'dt': np.repeat(read['dt'], read_cnt_by_user),
                         'hr': np.repeat(read['hr'], read_cnt_by_user),
                         'user_id': np.repeat(read['user_id'], read_cnt_by_user),
                         'article_id': chainer(read['article_id'])})
read_raw = read_raw.reset_index(drop=True)
read_raw['article'] = read_raw['article_id'].apply(lambda x: str(x).split('_')[0])
del read

user = pd.read_csv(path + 'users.csv')
dev = pd.read_csv(path + 'dev.csv')
test = pd.read_csv(path + 'test.csv')
metadata = pd.read_json('rawdata/metadata.json', lines=True)
magazine = pd.read_json('rawdata/magazine.json', lines=True)
metadata = pd.merge(metadata, magazine.rename(columns={'id':'magazine_id'}), how='left', on='magazine_id')
metadata['reg_ts'] = metadata['reg_ts'].apply(lambda x: int(datetime.datetime.fromtimestamp(x/1000).strftime('%Y%m%d')))


# # basic preprocess

# In[3]:


# metadata에 존재하는 작품만
read_raw = read_raw[read_raw['article_id'].isin(metadata['id'].unique())].reset_index(drop=True)

# 2월 18일 이후의 read data만
read_raw2 = read_raw[read_raw['dt']>=20190224].reset_index(drop=True)

# read data 중 5개 이상 글을 소비한 유저만
# read_raw2 = read_raw2[read_raw2['user_id'].isin(read_raw2.groupby('user_id')['dt'].count()[read_raw2.groupby('user_id')['dt'].count() > 4].index)].reset_index(drop=True)

# popular agg data
# read_raw4 = read_raw2[~((read_raw2['article'].isin(read_raw2['article'].value_counts().head(5).index)) & (read_raw2['dt']<=20190220))].reset_index(drop=True)

# # read data 중 unique
# read_raw3 = read_raw[['user_id', 'article_id']].drop_duplicates()

# # metadata 18일 이후와 3월 15일 이전으로
metadata['article'] = metadata['user_id'].astype(str) +'_'+metadata['magazine_tag_list'].astype(str)
metadata2 = metadata[(metadata['reg_ts']>=20190301) & (metadata['reg_ts']<20190315)].reset_index(drop=True)

# # dev data에 following data 추가
# dev2 = pd.merge(dev, user[['following_list', 'id']], how='left', on='id')

user2 = user[user['id'].isin(test['id'])].reset_index(drop=True)


# In[4]:


read_raw3 = pd.merge(read_raw2.drop('article', axis=1), metadata[['id', 'article']].rename(columns={'id':'article_id'}), how='left', on='article_id')
read_raw3 = read_raw3.drop_duplicates().reset_index(drop=True)
popular_list = read_raw3['article'].value_counts()[2:].index


# In[5]:


test['recommend']=''
for idx in tqdm_notebook(range(len(test))):
    user_id = pd.Series(test.loc[idx, 'id'])
    
    follow = user2.loc[user2['id'].isin(user_id), 'following_list']
    history = read_raw3[read_raw3['user_id'].isin(user_id)]
    
    recommend = ['@brunch_153']
    
    # history
    history_based_recommend = metadata2[metadata2['article'].isin(history['article'].value_counts().index[history['article'].value_counts()>1])].sort_values('reg_ts')['id'].tolist()
    history_based_recommend = pd.Series(history_based_recommend)[~pd.Series(history_based_recommend).isin(recommend)].tolist()
    recommend.extend(history_based_recommend)
    
    # follow
    if len(follow)>0:
        follow_based_recommend = metadata.loc[metadata['user_id'].isin(eval(follow.values[0])), 'article']
        recommend_article = popular_list[popular_list.isin(follow_based_recommend)]
        follow_based_recommend = metadata2[metadata2['article'].isin(recommend_article)].sort_values('reg_ts')['id']
        follow_based_recommend = follow_based_recommend[~follow_based_recommend.isin(recommend)].tolist()
        recommend.extend(follow_based_recommend)
    
    test.loc[idx, 'recommend'] = recommend


# In[6]:


test['submit'] = test['id'] + ' ' + test['recommend'].apply(lambda x: ' '.join(x))
test['submit'].to_csv('data/inferencefile/recommend.csv', index=False)


# In[7]:


print('100개가 완벽히 추천된 아이템 개수 : {} \n추천된 item의 unique개수 : {} - entropy와 밀접한 관련'.format(
    sum(test['submit'].apply(lambda x: len(x.split(' ')))==101), len(np.unique([j for i in test['recommend'] for j in i]))))


# In[8]:


# version10을 보면 추천 이상하게 한거 있음
# version4를 보면 옛날 코드가 있습니다.

