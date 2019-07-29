
# In[6]:
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
import matplotlib.font_manager as fm
from pytz import timezone, utc

# In[7]:


path1 = 'rawdata/'

users = pd.read_json(path1 + 'users.json', lines=True)

dev = pd.read_csv(path1+'predict/dev.users', names=['id'])
test = pd.read_csv(path1+'predict/test.users', names=['id'])


# In[9]:


path2 = path1 + 'read/'
read_file_lst = os.listdir(path2)
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
read = read[read['article_id']!='']


# In[10]:


output_path = 'data/'


# In[11]:

print('data/users.csv 생성완료')
print('data/dev.csv 생성완료')
print('data/test.csv 생성완료')
print('data/read.csv 생성완료')
users.to_csv(output_path + 'users.csv', index=False)
dev.to_csv(output_path + 'dev.csv', index=False)
test.to_csv(output_path + 'test.csv', index=False)
read.to_csv(output_path + 'read.csv', index=False)


# In[ ]:




