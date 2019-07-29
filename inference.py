#!/usr/bin/env python
# coding: utf-8

# In[2]:


import pandas as pd
import numpy as np
import os
import tqdm

# In[3]:


path = 'data/'
os.listdir(path)


# In[4]:


metadata = pd.read_csv(path + 'metadata_test.csv', header=None)
metadata.columns = ['id']

mf = pd.read_csv('pretrained/mf_test.csv', header=None)
march = pd.read_csv(path+ 'march_recommend_test.csv', header=None)
follow = pd.read_csv(path + 'follow_test.csv', header=None)
wr = pd.read_csv(path + 'wr_test.csv', header=None)




# In[45]:


def cleaning(rec):
    rec['id'] = rec[0].apply(lambda x: str(x).split(' ')[0])
    rec['recommend'] = rec[0].apply(lambda x: str(x).split(' ')[1:])
    return rec.iloc[:, 1:]


# In[46]:


mf = cleaning(mf)
march = cleaning(march)
follow = cleaning(follow)
wr = cleaning(wr)


# In[47]:


mf['submit']=''
for idx in tqdm.tqdm(range(len(mf))):
    
    a = march.loc[idx, 'recommend']
    b = mf.loc[idx, 'recommend'][:20]
    c = follow.loc[idx, 'recommend']
    d = wr.loc[idx, 'recommend'][:20]

    recommend_list = []
    recommend_list.extend([a[0]])
    a = a[1:]

    while True:
        try:
            recommend_list.extend(c[:2])
            c = c[2:]
            recommend_list.extend(b[:2])
            b = b[2:]
        except:
            pass
        if len(c)+len(b)==0:
            break
            
    recommend_list = pd.Series(recommend_list).unique().tolist()
    
    recommend_list3 = []
    while True:
        try:
            recommend_list3.extend(recommend_list[:2])
            recommend_list = recommend_list[2:]
            recommend_list3.extend(d[:2])
            d = d[2:]
        except:
            pass
        if len(recommend_list)+len(d)==0:
            break
            
    recommend_list = pd.Series(recommend_list3).unique().tolist()

    recommend_list2 = []
    while True:
        try:
            recommend_list2.extend(recommend_list[:2])
            recommend_list = recommend_list[2:]
            recommend_list2.extend(a[:2])
            a = a[2:]
        except:
            pass
        if len(recommend_list2)>=100:
            break
    
    recommend_list2 = pd.Series(recommend_list2).unique().tolist()[:80]
    mf.loc[idx, 'submit'] = recommend_list2


# In[48]:


rec_list = np.unique([j for i in mf['submit'] for j in i])
rec_list_market = metadata.loc[~metadata['id'].isin(rec_list), 'id'].unique()


# In[50]:


import random
random.seed(42)
random.shuffle(rec_list_market)
for idx in range(len(mf)):
    recommend_list = mf.loc[idx, 'submit']
    recommend_list.extend(rec_list_market[:20].tolist())
    rec_list_market = rec_list_market[20:]
    mf.loc[idx, 'submit'] = recommend_list


# In[54]:


dev = mf
dev = dev.drop(columns=['recommend']).rename(columns={'submit':'recommend'})
dev['submit'] = dev['id'] + ' ' + dev['recommend'].apply(lambda x: ' '.join(x))
dev['submit'].to_csv('inference/recommend.csv', index=False, header=False)


print('100개가 완벽히 추천된 아이템 개수 : {} \n추천된 item의 unique개수 : {} - entropy와 밀접한 관련'.format(
    sum(dev['submit'].apply(lambda x: len(x.split(' ')))==101), len(np.unique([j for i in dev['recommend'] for j in i]))))


# In[ ]:




