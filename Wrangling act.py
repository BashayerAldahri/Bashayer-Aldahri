#!/usr/bin/env python
# coding: utf-8

# # Data Gathring

# In[280]:


import pandas as pd
import requests
import json
import numpy as np
import matplotlib.pyplot as plt


# In[212]:


twitter_archive=pd.read_csv('twitter-archive-enhanced.csv')
twitter_archive.info()


# In[213]:


url='https://d17h27t6h515a5.cloudfront.net/topher/2017/August/599fd2ad_image-predictions/image-predictions.tsv'
r=requests.get(url)

with open(url.split('/')[-1], 'wb') as file:
    file.write(r.content)


# In[214]:


image_predictions= pd.read_csv('image-predictions.tsv', sep = '\t', encoding = 'utf-8')


# In[215]:


data = []

with open('tweet-json.txt') as json_file:
    for each_dict in json_file:
        data.append(json.loads(each_dict))
        
tweets = DataFrame (data)


# # Data Assessing
# 

# In[216]:


tweets


# In[217]:


tweets.info()


# In[218]:


tweets_new=tweets[['id','full_text','favorite_count','retweet_count','source','lang']]


# In[219]:


tweets_new


# In[220]:


tweets_new.info()


# In[221]:


image_predictions.info()


# In[222]:


image_predictions[image_predictions.jpg_url.duplicated()]


# In[223]:


twitter_archive.info()


# ### Isuess 
# 
# #### Quality issues
# 
# - Change Id data type to String instead of integer.
# - Change the name of columns --> ["Lang", "Full Text"].
# - Change the name of columns in image_predictions
# - Seprate Url form Source and let the source in Device column  ----> tweets_new Table.
# - Drop duplicate data in df table ----> Camela, Corgi.
# - Wronge data in name column.
# - The rating rating_numerator should be out of 13.
# - Collect necessary columns for twitter-archive-enhanced table and tweet_json "tweets" table 
# - Delete duplicate in jpg_url.
# - Change data type of rating_numerator to float
# - Change data type of rating_denominator to float
# 
# #### Tidiness issues
# - Let dogs stage in one column, I going to call it "Dogs Stage".
# - Merging. 

# ### Data Cleaning 

# In[224]:


tweets_new['id'] = tweets_new['id'].astype(str)


# In[225]:


tweets_new.info()


# In[324]:


tweets_new.rename(columns={'id' : 'tweet_id','lang':'Language', 'full_text' : 'Tweets_text'}, inplace=True)


# In[325]:


tweets_new.info()


# In[228]:


tweets_new['source'].value_counts()


# In[229]:


import re

Extract = ['Twitter for iPhone','Vine - Make a Scene','Twitter Web Client','TweetDeck']
pat = '|'.join(r"\b{}\b".format(x) for x in Extract)

tweets_new['Device'] = tweets_new['source'].str.extract('('+ pat + ')', expand=False, flags=re.I)
print (tweets_new)


# In[231]:


tweets_new.drop(['source'], axis=1)


# In[232]:


tweets_new['Device'].value_counts()


# In[233]:


twitter_archive


# In[234]:


import re

Extract = ['Twitter for iPhone','Vine - Make a Scene','Twitter Web Client','TweetDeck']
pat = '|'.join(r"\b{}\b".format(x) for x in Extract)

twitter_archive['Device'] = twitter_archive['source'].str.extract('('+ pat + ')', expand=False, flags=re.I)
print (twitter_archive)


# In[236]:


twitter_archive['Device'].value_counts()


# In[309]:


twitter_archive.drop(['source'], axis=1)


# In[321]:





# In[322]:


twitter_archive['Dogs_Stage'] = twitter_archive[['doggo', 'floofer','floofer','puppo']].apply(lambda x: ' '.join(x), axis = 1)
print(twitter_archive)


# In[336]:


twitter_archive_new=twitter_archive[['tweet_id','timestamp','expanded_urls','name','Dogs_Stage','rating_numerator','rating_denominator']]
twitter_archive_new


# In[337]:


twitter_archive_new['Dogs_Stage'].value_counts()


# In[338]:


twitter_archive_new.info()


# In[339]:


twitter_archive_new[['rating_numerator', 'rating_denominator']] = twitter_archive_new[['rating_numerator', 'rating_denominator']].astype(float)


# In[340]:


twitter_archive_new['timestamp']=pd.to_datetime(twitter_archive_new['timestamp'])


# In[341]:


twitter_archive_new['tweet_id'] = twitter_archive_new['tweet_id'].astype(str)


# In[342]:


twitter_archive_new.info()


# In[343]:


twitter_archive_new


# In[344]:


image_predictions


# In[345]:


image_predictions['tweet_id'] = image_predictions['tweet_id'].astype(str)


# In[346]:


image_predictions.rename(columns={'p1':'prediction1_for_the_image', 'p1_conf' : 'confident_for_prediction1','p1_dog' : 'prediction1_dog','p2' : 'prediction2_for_the_image','p2_conf' : 'confident_for_prediction2', 'p2_dog' : 'prediction2_dog','p3' : 'prediction3_for_the_image','p3_conf' : 'confident_for_prediction3', 'p3_dog' : 'prediction3_dog' }, inplace=True)


# In[347]:


#Merge twitter_archive_new and image_predictions

df_merge_tables = pd.merge(twitter_archive_new, image_predictions,how='left', on=['tweet_id']) 


df_merge_tables = df_merge_tables[df_merge_tables['name'].notnull()]

df_merge_tables.info()


# In[348]:


twitter_archive_master = pd.merge(df_merge_tables, tweets_new,how='left', on=['tweet_id'])

    
    
twitter_archive_master.info()


# In[349]:


twitter_archive_master = tables.dropna(how='any',axis=0)

twitter_archive_master.info()


# In[350]:


#Store data


twitter_archive_master.to_csv('twitter_archive_master.csv', encoding='utf-8')


twitter_archive_master


# ## Visualization 

# In[354]:


## What the most source of tweets 

twitter_archive_master = twitter_archive_master.groupby('Device').filter(lambda x: len(x) >=20)
twitter_archive_master['Device'].value_counts().plot(kind = 'pie')


plt.title("The most source of tweets")
plt.xlabel("")
plt.ylabel("")


# In[364]:


## What the most source of tweets 

twitter_archive_master = twitter_archive_master.groupby('prediction1_for_the_image').filter(lambda x: len(x) >=20)
twitter_archive_master['prediction1_for_the_image'].value_counts().plot(kind = 'pie')


plt.title("The most source of tweets")
plt.xlabel("")
plt.ylabel("")


# In[356]:


from subprocess import call 
call(['python', '-m', 'nbconvert', 'Wrangling act.ipynb'])


# In[ ]:




