from langdetect import detect
import nltk 
nltk.download('stopwords')
from nltk.corpus import stopwords
import pandas as pd
import preprocessor as p
import random
import re
import spacy

# import the list of cognition (reasoning) words from .txt; one word each line
f = open('cognition_list.txt','r')
cognition_list = f.read().split('\n')
f.close()

# import the list of affection (emotion) words from .txt; one word each line
f = open('affect_list.txt','r')
affect_list = f.read().split('\n')
f.close()

# import tweet data from .csv
df = pd.read_csv("ExtractedTweets.csv")

# import the list of English stopwords from NLTK's stopwords
stopword = set(stopwords.words("english"))

# function to clean tweet:
def cleanTweet(tweet):
    tweet = tweet.lower() # lowercase
    tweet = re.sub('#', '', p.clean(tweet)) # get text from hashtag after tweet being preprocessed by package preprocessor (p)
    tweet = re.sub("[^a-z\s]", "" , tweet) # remove special characters and numbers
    tweet = " ".join(word for word in tweet.split() if word not in stopword) # remove stopwords
    return tweet

# load SpaCy package
nlp = spacy.load("en_core_web_lg")

### package preprocessor: set option to remove hashtags
p.set_options(p.OPT.URL, p.OPT.EMOJI, p.OPT.MENTION, p.OPT.HASHTAG)

# cognition and affection scores CHANGE IF INCLUDE HASHTAG
cognition_score = []
affection_score = []

nlp_cognition = nlp(' '.join(cognition_list))
nlp_affection = nlp(' '.join(affect_list))

# for each tweet, record its word vector's similarity to (average) cognition vector
for i in range(len(df['Tweet'])):
    nlp_tweet = nlp(cleanTweet(df['Tweet'][i]))
    cognition_score.append(nlp_cognition.similarity(nlp_tweet))
    affection_score.append(nlp_affection.similarity(nlp_tweet))

# record the affection score and cognition score to df
df['affection'] = affection_score
df['cognition'] = cognition_score

# record the smoothened affection:cognition score ratio to df
df['ratio'] = (df['affection'] + 1) / (df['cognition'] + 1)

# number of tokens used CHANGE IF INCLUDE HASHTAG
num_token = []
for i in range(len(df['Tweet'])):
    nlp_tweet = nlp(cleanTweet(df['Tweet'][i]))
    num_token.append(len(nlp_tweet))

# record the number of tokens to df
df['token'] = num_token

# computes the language of the tweet using package langdetect
language = []
for i in range(len(df['Tweet'])):
    if cleanTweet(df['Tweet'][i]) != '':
        language.append(detect(cleanTweet(df['Tweet'][i])))
    else:
        language.append('en')

# record the language to df
df['language'] = language

# for each party, compute its most emotional tweets randomly chosen 10 from top 5%
# chosen from those with at least 4 tokens (otherwise, too little context)
for party in ['Democrat', 'Republican']:
    x = df[(df['language'] == 'en') & (df['token'] > 4) & (df['Party'] == party)].sort_values('ratio', ascending = False).head(int(len(df)*(5/100)))['Tweet']
    y = random.sample(list(x), 10)
    
    # write out the file .txt
    filename = "mostemotional_" + party + "_nohashtag.txt"
    f = open(filename, "a", encoding = 'utf-8')
    f.write('\n'.join(y))
    f.close()

# for each party, compute its least emotional tweets randomly chosen 10 from top 5%
# chosen from those with at least 4 tokens (otherwise, too little context)
for party in ['Democrat', 'Republican']:
    x = df[(df['language'] == 'en') & (df['token'] > 4) & (df['Party'] == party)].sort_values('ratio', ascending = False).tail(int(len(df)*(5/100)))['Tweet']
    y = random.sample(list(x), 10)
    
    # write out the file .txt
    filename = "leastemotional_" + party + "_nohashtag.txt"
    f = open(filename, "a", encoding = 'utf-8')
    f.write('\n'.join(y))
    f.close()
    
### option with strings in hashtag
p.set_options(p.OPT.URL, p.OPT.EMOJI, p.OPT.MENTION)

# cognition and affection scores CHANGE IF INCLUDE HASHTAG
cognition_score_hashtag = []
affection_score_hashtag = []

nlp_cognition_hashtag = nlp(' '.join(cognition_list))
nlp_affection_hashtag = nlp(' '.join(affect_list))

for i in range(len(df['Tweet'])):
    print(i)
    nlp_tweet = nlp(cleanTweet(df['Tweet'][i]))
    cognition_score_hashtag.append(nlp_cognition_hashtag.similarity(nlp_tweet))
    affection_score_hashtag.append(nlp_affection_hashtag.similarity(nlp_tweet))
    
df['affection_hashtag'] = affection_score_hashtag
df['cognition_hashtag'] = cognition_score_hashtag
df['ratio_hashtag'] = (df['affection_hashtag'] + 1) / (df['cognition_hashtag'] + 1)
df.head()

# num token CHANGE IF INCLUDE HASHTAG
num_token_hashtag = []
for i in range(len(df['Tweet'])):
    print(i)
    nlp_tweet = nlp(cleanTweet(df['Tweet'][i]))
    num_token_hashtag.append(len(nlp_tweet))
    
df['token'] = num_token_hashtag

# for each party, compute its most emotional tweets randomly chosen 10 from top 5%
# chosen from those with at least 4 tokens (otherwise, too little context)
for party in ['Democrat', 'Republican']:
    x = df[(df['language'] == 'en') & (df['token'] > 4) & (df['Party'] == party)].sort_values('ratio_hashtag', ascending = False).head(int(len(df)*(5/100)))['Tweet']
    y = random.sample(list(x), 10)
    
    # write out the file .txt
    filename = "mostemotional_" + party + "_withhashtag.txt"
    f = open(filename, "a", encoding = 'utf-8')
    f.write('\n'.join(y))
    f.close()

# for each party, compute its least emotional tweets randomly chosen 10 from top 5%
# chosen from those with at least 4 tokens (otherwise, too little context)
for party in ['Democrat', 'Republican']:
    x = df[(df['language'] == 'en') & (df['token'] > 4) & (df['Party'] == party)].sort_values('ratio_hashtag', ascending = False).tail(int(len(df)*(5/100)))['Tweet']
    y = random.sample(list(x), 10)
    
    # write out the file .txt
    filename = "leastemotional_" + party + "_withhashtag.txt"
    f = open(filename, "a", encoding = 'utf-8')
    f.write('\n'.join(y))
    f.close()
    
###################### HASHTAG #######################
# in each tweet, find all hashtags
hashtags = []
for i in range(len(df['Tweet'])):
    hashtags.append(" ".join(re.findall("#(\w+)", df['Tweet'][i])))
    
# in each tweet, record the number of hashtags
hashtags_length = []
for i in range(len(df['Tweet'])):
    hashtags_length.append(len(re.findall("#(\w+)", df['Tweet'][i])))

# record hashtags and the number of them to df
df['hashtags'] = hashtags
df['hashtags_length'] = hashtags_length

dfRT = df[(df['language'] == 'en') & (df['token'] > 4) & (df['hashtags_length'] > 0) & (df['Party'] == 'Republican')].sort_values('ratio_hashtag', ascending = False).tail(int(len(df)*(5/100)))
dfRH = df[(df['language'] == 'en') & (df['token'] > 4) & (df['hashtags_length'] > 0) & (df['Party'] == 'Republican')].sort_values('ratio_hashtag', ascending = False).head(int(len(df)*(5/100)))
dfDT = df[(df['language'] == 'en') & (df['token'] > 4) & (df['hashtags_length'] > 0) & (df['Party'] == 'Democrat')].sort_values('ratio_hashtag', ascending = False).tail(int(len(df)*(5/100)))
dfDH = df[(df['language'] == 'en') & (df['token'] > 4) & (df['hashtags_length'] > 0) & (df['Party'] == 'Democrat')].sort_values('ratio_hashtag', ascending = False).head(int(len(df)*(5/100)))

numRT = (1 + sum(pd.Series(dfRT['hashtags']).str.contains(hashtag)))
numRH = (1 + sum(pd.Series(dfRH['hashtags']).str.contains(hashtag)))
numDT = (1 + sum(pd.Series(dfDT['hashtags']).str.contains(hashtag)))
numDH = (1 + sum(pd.Series(dfDH['hashtags']).str.contains(hashtag)))

denRT = len(dfRT['hashtags'])
denRH = len(dfRH['hashtags'])
denDT = len(dfDT['hashtags'])
denDH = len(dfDH['hashtags'])

num = numRT + numRH + numDT + numDH
den = denRT + denRH + denDT + denDH

###
odd_ratio = []
hashtags = list(set(" ".join(x).split()))

# compute the odd-ratio for Republicans with lowest affection:cognition ratios against other types of hashtags
for hashtag in hashtags:
    p = numRT / denRT
    q = (num - numRT) / (den - denRT)
    odd_ratio.append((p/(1 - p))/(q/(1 - q)))

y = pd.DataFrame({"hashtag": hashtags, "odd_ratio": odd_ratio}).sort_values('odd_ratio', ascending = False).head(20)['hashtag']
    
# write out the file .txt
filename = "highestoddratiohashtag_" + "RepublicanTail" + ".txt"
f = open(filename, "a", encoding = 'utf-8')
f.write('\n'.join(y))
f.close()

###
odd_ratio = []
hashtags = list(set(" ".join(x).split()))

# compute the odd-ratio for Republicans with highest affection:cognition ratios against other types of hashtags
for hashtag in hashtags:
    p = numRH / denRH
    q = (num - numRH) / (den - denRH)
    odd_ratio.append((p/(1 - p))/(q/(1 - q)))

y = pd.DataFrame({"hashtag": hashtags, "odd_ratio": odd_ratio}).sort_values('odd_ratio', ascending = False).head(20)['hashtag']
    
# write out the file .txt
filename = "oddratiohashtag_" + "RepublicanHead" + ".txt"
f = open(filename, "a", encoding = 'utf-8')
f.write('\n'.join(y))
f.close()

###
odd_ratio = []
hashtags = list(set(" ".join(x).split()))

# compute the odd-ratio for Democrats with hightest affection:cognition ratios against other types of hashtags
for hashtag in hashtags:
    p = numDH / denDH
    q = (num - numDH) / (den - denDH)
    odd_ratio.append((p/(1 - p))/(q/(1 - q)))

y = pd.DataFrame({"hashtag": hashtags, "odd_ratio": odd_ratio}).sort_values('odd_ratio', ascending = False).head(20)['hashtag']
    
# write out the file .txt
filename = "oddratiohashtag_" + "DemocratHead" + ".txt"
f = open(filename, "a", encoding = 'utf-8')
f.write('\n'.join(y))
f.close()

###
odd_ratio = []
hashtags = list(set(" ".join(x).split()))

# compute the odd-ratio for Democrats with lowest affection:cognition ratios against other types of hashtags
for hashtag in hashtags:
    p = numDT / denDT
    q = (num - numDT) / (den - denDT)
    odd_ratio.append((p/(1 - p))/(q/(1 - q)))

y = pd.DataFrame({"hashtag": hashtags, "odd_ratio": odd_ratio}).sort_values('odd_ratio', ascending = False).head(20)['hashtag']
    
# write out the file .txt
filename = "oddratiohashtag_" + "DemocratTail" + ".txt"
f = open(filename, "a", encoding = 'utf-8')
f.write('\n'.join(y))
f.close()