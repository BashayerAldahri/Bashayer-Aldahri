# Data Wrangling Steps 



# These are the requied libraries, json to read json file, pandas to read CSV file and request to request url 

import pandas as pd
import requests
import json
import numpy as np
import matplotlib.pyplot as plt


# to request url

url='https://d17h27t6h515a5.cloudfront.net/topher/2017/August/599fd2ad_image-predictions/image-predictions.tsv'
r=requests.get(url)

with open(url.split('/')[-1], 'wb') as file:
    file.write(r.content)
    
# To read Json file 

data = []

with open('tweet-json.txt') as json_file:
    for each_dict in json_file:
        data.append(json.loads(each_dict))
        
tweet_json = pd.DataFrame(data)


# After Wrangling the data, I marge all the data sources in one dataframe and then save it on CSV file
# If you have any Q, contact me on Email
# Thank you 


