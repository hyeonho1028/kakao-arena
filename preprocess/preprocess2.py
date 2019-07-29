#!/usr/bin/env python
# coding: utf-8

# In[1]:


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
from pytz import timezone, utc


# 1. pop_writer_article.json 
# 2. all_test_history.json o 
# 3. 0222_0301_1000_recommend.txt o
# 4. 18_read_raw.csv ---------------- o
# 
# 
# 1. test.users
# 2. recommend_art_51.txt
# 3. recommend_57_test.txt

# In[2]:
KST = timezone('Asia/Seoul')






# read data
path2 = 'rawdata/read/'
read_file_lst = pd.read_csv('rawdata/read_data_sort.csv', header=None)[0].tolist()
exclude_file_lst = ['read.tar', '.2019010120_2019010121.un~']
read_df_lst = []
for f in read_file_lst:
    file_name = os.path.basename(f)
    if file_name in exclude_file_lst:
        print(file_name)
    else:
        df_temp = pd.read_csv(path2+f, header=None, names=['raw'])
        df_temp['dt'] = file_name[:8]
        df_temp['hr'] = file_name[8:10]
        df_temp['user_id'] = df_temp['raw'].str.split(' ').str[0]
        df_temp['article_id'] = df_temp['raw'].str.split(' ').str[1:].str.join(' ').str.strip()
        read_df_lst.append(df_temp)
        
read = pd.concat(read_df_lst)

def chainer(s):
    return list(chain.from_iterable(s.str.split(' ')))
read_cnt_by_user = read['article_id'].str.split(' ').map(len)
read_raw = pd.DataFrame({'dt': np.repeat(read['dt'], read_cnt_by_user),
                         'hr': np.repeat(read['hr'], read_cnt_by_user),
                         'user_id': np.repeat(read['user_id'], read_cnt_by_user),
                         'article_id': chainer(read['article_id'])})


read_raw2= read_raw[read_raw['article_id']!='']



# In[3]:


# test 정보
test = pd.read_csv('rawdata/predict/test.users',names=['id'])
test_list = test['id'].values.tolist()


# In[4]:


"""18_read_raw.csv 만들기"""



past_df2 = read_raw2[read_raw2.dt.astype('int32')>=20190218].sort_values(['dt', 'hr'])
author = past_df2.article_id.values.tolist()
past_df2['author'] = [x.split('_')[0] for x in author]

past_df2.to_csv('data/18_read_raw.csv',index=False)
print('data/18_read_raw.csv 생성완료')

# In[ ]:


"""all test history 만들기"""
all_test_history={}

dp_df = read_raw2.drop(['dt','hr'],axis=1).drop_duplicates()

for i in tqdm(test_list):
    all_test_history[i]=dp_df[dp_df.user_id.isin([i])].article_id.unique().tolist()
    
"""저장"""
data1={}
data1['all_test_history'] = all_test_history

with open('data/all_test_history.json', 'w', encoding="utf-8") as make_file:
    json.dump(data1, make_file, ensure_ascii=False, indent="\t")
print('data/all_test_history.json 생성완료')

# In[153]:


"""pop article 만들기"""


import datetime

metadata = pd.read_json('rawdata/metadata.json',lines=True)
new_metadata = metadata.copy()

time=[]


for i in metadata.reg_ts:
    time.append(int(datetime.datetime.fromtimestamp(i/1000,KST).strftime('%Y%m%d')))
    
new_metadata['time'] = time

metadata_save = new_metadata.copy()

new_metadata = new_metadata[(new_metadata.time >= 20190301)&(new_metadata.time <= 20190314)]
author2 = new_metadata.id.values.tolist()
new_metadata['author'] = [x.split('_')[0] for x in author2]


# In[5]:

df = read_raw2.copy()
df.dt = df.dt.astype('int32')
df_22 = df[df.dt>=20190222]
author = df_22.article_id.values.tolist()
df_22['author'] = [x.split('_')[0] for x in author]
df_22 = df_22[['article_id','author']]


# In[6]:


pop_writer_article={}

isin={}
for i in metadata.id.values:
    isin[i] = 1
    
for i in tqdm(df_22.author.unique()):
    count=Counter(df_22[df_22.author.isin([i])].article_id).most_common()
    pop_writer_article[i]=[x for x in count if x[0] in isin]


# In[7]:


delete=['#d6a2d0cfebc30014e9b0d9e82c21e6a9', '#b775dd5e306524d79dd0bb86f5b59597', '#026ba00d4f6cac8a4139429203792854', '#1309bc3e76f84cb82b33d93f8aacad96',
 '#ccf27ca1493c95d0e106b0b68ab9c7e8', '#e9b3bb3be1de0dcdf09be598cbdc9eba', '#5459ac2d70cf188ed7923383def0cefc', '#00700c454af49d5c9a36a13fcba01d0a',
 '#5569d6f44ccee9e112849a84b4c1112e', '#e59ec7aac131002599aaa57a93133453', '#d17aad82f76714b2c6c5938c1b795d28', '#8432c559c6adb805190812275b667177',
 '#13319c572752adddb2a6288bedfe1e62', '#c491f693c5c44220fcf85eb15d5c4110', '#c312c051de62857bdb28fcc981141c56', '#17891e1798aeb4a7a6c8e89db054192e',
 '#cb56c6b1805825f05bbd862cc5d93693', '#bd2bdfcf6d761273e6ed680c5428fd49', '#8994e49dba4a538b8527597268df8fc5', '#d05721e8e171e2b1d0a0660b763249d8',
 '#0575540a724efe88bbaf1b05e39a35e3', '#6afdaa1977750acce82773572d21c53d', '#59d0ed04b8aa7ee9c1b45f9a96022212', '#19d99322e893100d6830cfe3b93ac403',
 '#1d489713329b02507db6fdb9121b6864', '#e864c90f67705fb5b59ca4b0baec31e5', '#b79375f48c55ce2902e30352cc65a945', '#ea457870a2d32453609f52e50f84abdc',
 '#4043a59d3e22c68ad7eae38e593b7730', '#fa884ed07642aeaad911b1081876ba7b', '#a46c7024b3804ab1f4fd549e4d9448bb', '#402e1d254e744932688bdac511814a6b',
 '#ab8c84a03bed3e98731cf8a4e2218b23', '#b925ff0cdcca05d6802c440efa00c0d1', '#72699582d9013ba3389dfd2e520557e1', '#db8f8c504893d3513ccdbc93e46d6347',
 '#d55eb8f352a00a50d07d343f73b02a24', '#eea417f933b7266688ad631a8376149f', '#395b8837765e31ee4194e07d89e0c9c6', '#2e004caa3aecf4fc5d651cfaaf28d43c',
 '#6eb349ad62c019fa367d42949288d1dc', '#03f971237623f15812093fa868f3890d', '#0bd5d8012d1594dc0ef520ab70dbab96', '#b8f9863df77729ad82ecf089d28deaac',
 '#7e1190ae644e0e613250ec25096e4711', '#25fb3334a08a466c9eb493279f5ded1d', '#01d75a6a98719f0a7f111b7eacd51080', '#372b1435b88db8569c8074862f610151',
 '#e35c0f6ba0354c38f3471cbdf23bf3b9', '#f8e1dfcbedd9ed423d2c877cb30b0793', '#237958c1ca06f81d70d492525833ce7c', '#6575042680464e111fb5d911cd86bd28',
 '#da86886aae02dcae9bd44f8098a39832', '#2c316f1b18a85c76e3a5ebb79aadf296', '#0f7dfd859efbb79bd92b8d853a81250d', '#45dd173ec1a1f478f729590e02d7e8c6',
 '#0f8b4b27d904f970ffe4b7bf3e97d699', '#4841af244ff19f96fb3f6077b230526c', '#ba915261778727c191eb77848288a92a', '#fb947c08f37d20f01fa0617a02d2ee21',
 '#e2d7ad8dbb1f5ec0368f4ec5efdfae0d', '#c6929d4aca853d6b67b5104f1185eeca', '#46299aafa81870e19d00764047631c3f', '#b7e863c99ef486767999f11f7ccde513',
 '#e7053f7ff10b0d439592ca4a14ae75e2', '#16e48849be03333ead6fc6632c75ce52', '#81a9e9911e5ca57fbb1bf8293646736f', '#37031912c4a8126b6c7dde78e4f606c1',
 '#06ff288571e0b4e14a15c9e52dc48cdf', '#3c929226fd91cc088de315d3386abb1f', '#a8c4e60f2d8365ee7755ef27838c02c0', '#599fe1d0d696abb4c33e145f46b5616c',
 '#3b9412b86884b63807e2b92faf17b983', '#63fcd27f017d062ba3897d74a8a8f873', '#86c33e4dc465782c694e52362d7d3470', '#66635653185b678a241a5d393d5c9d49',
 '#aebac45e65ac7018ffe11f8c14c926b6', '#b8a2bfa4b6acba8123a705d61f053be9', '#388c19d65d194f07589aa79342d23d75', '#4a52d6e45528fd2bd2da60f7b4e45384',
 '#aacab0a09df0f45d435ac5a8ea6c1075', '#4684641f62d7c1746a1096b8c438514e', '#e8549f0b63591f5e7decf68105e1eb0f', '#f8f99d94518336c342d74bcdfb764496',
 '#85e853f5d3253653c886a89343b4618c', '#d0d9fad6be6f1f4c23746b57842c811a', '#7d8d5a97a6af137a28904ee5b8640b65', '#24479d076bad15d8dc02c4f6d10c156b',
 '#890f3ee19f4f054baac3d1f99049c90c', '#90857e0913d21a0a72a2d517831b50b1', '#8a1720441dc2ea8a489776fc45177de8', '#db0b012d743e033df05f61bee6b8709b',
 '#ba364c1064236b8028b6d271307662cf']


# In[8]:


a = [x for x in pop_writer_article if x not in delete]
new_pop_writer_article ={}
for i in a:
    new_pop_writer_article[i] = pop_writer_article[i]


# In[9]:


c=new_metadata.author.unique()
past_df = df[df.dt>=20190222]
author3 = past_df.article_id.values.tolist()
past_df['author'] = [x.split('_')[0] for x in author3]
au = past_df.author.unique()
au2 = [x for x in au if x in c]

new_article={}
for i in new_metadata[new_metadata.author.isin(au2)].author:
    new=new_metadata[new_metadata.author.isin([i])].id.values.tolist()
    new_article[i] = [[x,1] for x in new]


# In[10]:


data1={}
data1['pop_writer_article'] = new_pop_writer_article
data1['new_article'] = new_article

with open('data/pop_writer_article.json', 'w', encoding="utf-8") as make_file:
    json.dump(data1, make_file, ensure_ascii=False, indent="\t")
print('data/pop_writer_article.json 생성완료')

# In[ ]:

metadata_save = metadata_save[(metadata_save['time']>=20180801) & (metadata_save['time']<20190315)]
metadata_save['id'].to_csv('data/metadata_test.csv', index=False)
print('data/metadata_test.csv 생성완료')

# In[ ]:




