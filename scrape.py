import pandas as pd
import json
import requests

api_key = 'd5e3da244db34daca7ac98b14139eb33'
headers = { 'Authorization' : 'd5e3da244db34daca7ac98b14139eb33'}

everything = 'https://newsapi.org/v2/everything?'


kwds = ['Apple']

sources = ['business-insider', 'google-news', 'financial-post',
           'reuters','nbc-news', 'techcrunch', 'the-wall-street-journal']

sortby = 'popularity'
params= {
    'q': kwds,
    'apiKey': api_key,
    'sortBy': sortby,
    'language': 'en',
    'page': 1
        }

response = requests.get(url=everything, headers=headers, params=params)

output = response.json()

articles = output['articles']

df = pd.DataFrame(articles)

df.to_csv('d1.csv')