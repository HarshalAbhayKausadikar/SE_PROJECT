import pandas as pd
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import spacy
import contextlib
import re
import csv


    #For classifying news into 5 categories, i.e, Very Negative, Negative, Neutral, Positive, Very Positive
def fine_grained_sentimental_analysis(content):   
    tokenizer = AutoTokenizer.from_pretrained("nlptown/bert-base-multilingual-uncased-sentiment")
    model = AutoModelForSequenceClassification.from_pretrained("nlptown/bert-base-multilingual-uncased-sentiment")   
    tokens = tokenizer.encode(content, return_tensors='pt', truncation=True, padding=True)
    result = model(tokens)
    result.logits
    sentiment_score = int(torch.argmax(result.logits))+1
    return sentiment_score

# load english language model and create nlp object from it
nlp = spacy.load("en_core_web_sm") 


#use this utility function to get the preprocessed text data
def preprocess(text):
    with contextlib.suppress(Exception):
        # remove special characters except full stop and apostrophe
        text = re.sub(r'[^a-zA-Z0-9\s.]', '', text)

        # text = text.lower()  # convert text to lowercase
        text = text.strip()  # remove leading and trailing whitespaces
        text = text.encode('ascii', 'ignore').decode('ascii')  # remove non-ascii characters

        # split text into words without messing up the punctuation
        text = re.findall(r"[\w']+|[.,!?;]", text)
    
        text= ' '.join(text)
        return text.replace(' .', '.')

def giveBaseScore(text):
    if(text == "Very Negative"):
        return 200
    
    elif(text == "Negative"):
        return 100
    
    return 0


def process_csv(filename):  
    with open ('wordstore/negative-words.txt', 'r', encoding='utf-8') as file:
        negative_words_list = file.read().splitlines()

    with open ('wordstore/bad-words.txt', 'r', encoding='utf-8') as file:
        bad_words = file.read().splitlines()

    with open ('wordstore/countries.txt', 'r', encoding='utf-8') as file:
        countries = file.read().splitlines()

    with open('wordstore/lawsuit.txt', 'r', encoding='utf-8') as file:
        lawsuits = file.read().splitlines()

    with open('wordstore/harassement.txt', 'r', encoding='utf-8') as file:
        harassment = file.read().splitlines()



# ========================#
# Creating Final csv      #
# ========================#
    #definig charset
    with open('COMMON-PROCESSED.csv', 'w', encoding='utf-8', newline='') as summary:
        
        # read first row from Uber.csv
        with open(filename, 'r', encoding='utf-8') as file:
            df_new = pd.read_csv(filename)
            df_new['preprocessed_content'] = df_new['description'].apply(preprocess)
            try:
                reader = csv.reader(file)
                next(reader)

                # write to csv
                writer = csv.writer(summary)

                # do for every news article
                writer.writerows([["Index","Source","Author","Title", "Description", "Content", "Headline Sentiment", "Offense Rating", "Negative Words", "Offensive Words", "Tags", "publishedAt", "url", "urlToImage"]])

                for idx, row in enumerate(reader, start=1):
                    raw_text = df_new['preprocessed_content'][idx]

                    sourceName = df_new['source'][idx]
                    sourceName = sourceName.split(',')[1][10:][:-2]

                    headline = df_new['title'][idx]
                    headline_sentiment = df_new['sentiment'][idx]
                    offense_rating = giveBaseScore(df_new['sentiment'][idx])

                    negative_words=[]
                    offensive_words=[]
                    tags=[]

                    published_date = df_new['publishedAt'][idx]
                    URL = df_new['url'][idx]
                    imageURL = df_new['urlToImage'][idx]


                    # tag as negative

                    nlp_text= nlp(raw_text)


                    # add custom entities
                    for word in nlp_text:
                        # if it is a negative word
                        if word.text.lower() in negative_words_list:
                            offense_rating+=10
                            negative_words.append(word.text)


                        # if it is a highly offensive word 
                        if word.text.lower() in bad_words:
                            offense_rating+=50
                            offensive_words.append(word.text)


                        # if the article is talks about lawsuits
                        if word.text.lower() in lawsuits:
                            offense_rating+=30
                            tags.append(word.text)

                        # if the article is about harassment
                        if word.text.lower() in harassment:
                            offense_rating+=50
                            tags.append(word.text)

                        # does article mention a country?
                        if word.text.lower() in countries:
                            tags.append(word.text)    

                        # does article mention a person
                        if word.ent_type_ == "PERSON":
                            tags.append(word.text) 
                        
                        if word.ent_type_ == "ORG":
                            tags.append(word.text)
                        
                        if word.ent_type_ == "GPE":
                            tags.append(word.text)


                    if offense_rating>20:
                        offense_rating-=10


                    # Write each row
                    writer.writerow(
                        [
                            idx,
                            sourceName,
                            df_new['author'][idx],
                            headline,
                            df_new['description'][idx],
                            df_new['content'][idx],
                            headline_sentiment,
                            offense_rating,
                            list(set(negative_words)),
                            list(set(offensive_words)),
                            list(set(tags)),
                            published_date,
                            URL,
                            imageURL,
                        ]
                    )
                    print(f"Article {idx} written to csv")

            except Exception as e:
                print(e)
                print(e.__class__)
                print(e.__doc__)
                print(e.__traceback__)

# def __init__(self):
#     self.fine_grained_sentimental_analysis(content)
#     self.giveBaseScore(text)
#     self.preprocess(text)
#     self.process_csv(filename)


df = pd.read_csv('news_data.csv')

df['preprocessed_title'] = df['title'].apply(preprocess)
print("Step 1\n")

df['score'] = df['preprocessed_title'].apply(fine_grained_sentimental_analysis)
print("Step 2\n")

df['score'].value_counts()

df['sentiment'] = df['score'].map({
    5: "Very Positive",
    4: "Positive",
    3: "Neutral",
    2: "Negative",
    1: "Very Negative"
})


df.to_csv('file.csv')
print("Step 3\n")
df_new = pd.read_csv('file.csv')

df_new['preprocessed_content'] = df_new['content'].apply(preprocess)
print("Step 4\n")
process_csv('file.csv')




