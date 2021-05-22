from langdetect import detect
import nltk 
nltk.download('stopwords')
from nltk.corpus import stopwords
import pandas as pd
import preprocessor as p
import random
import re
import spacy

class EmotionMeter:
    def __init__(self, data_path:str = "ExtractedTweets.csv"):
        self.data_path = data_path

    def load_cognition_list(self):
        # import the list of cognition (reasoning) words from .txt; one word each line
        f = open('cognition_list.txt','r')
        cognition_list = f.read().split('\n')
        f.close()
        return cognition_list

    def load_affection_list(self):
        # import the list of affection (emotion) words from .txt; one word each line
        f = open('affect_list.txt','r')
        affection_list = f.read().split('\n')
        f.close()
        return affection_list

    def load_data(self, data_path):
        # import tweet data from .csv
        # texts contain tweets on "Tweet" column!
        df = pd.read_csv(data_path)
        if "Tweet" not in df.columns():
            raise Exception("df must have column Tweet!")
        return df

    def preprocess_text(self, tweet, keep_hashtag_text:bool = False):
        # import the list of English stopwords from NLTK's stopwords
        stopword = set(stopwords.words("english"))
        if not keep_hashtag_text:
            p.set_options(p.OPT.URL, p.OPT.EMOJI, p.OPT.MENTION, p.OPT.HASHTAG)
        else:
            p.set_options(p.OPT.URL, p.OPT.EMOJI, p.OPT.MENTION)

        tweet = tweet.lower() # lowercase
        tweet = re.sub('#', '', p.clean(tweet)) # get text from hashtag after tweet being preprocessed by package preprocessor (p)
        tweet = re.sub("[^a-z\s]", "" , tweet) # remove special characters and numbers
        tweet = " ".join(word for word in tweet.split() if word not in stopword) # remove stopwords
        return tweet

    def calculate_score(self, df):
        # load SpaCy package
        nlp = spacy.load("en_core_web_lg")
        cognition_list = self.load_cognition_list()
        affect_list = self.load_affection_list()

        # cognition and affection scores CHANGE IF INCLUDE HASHTAG
        cognition_score = []
        affection_score = []

        nlp_cognition = nlp(' '.join(cognition_list))
        nlp_affection = nlp(' '.join(affect_list))

        # for each tweet, record its word vector's similarity to (average) cognition vector
        for i in range(len(df['Tweet'])):
            nlp_tweet = nlp(self.preprocess_text(df['Tweet'][i]))
            cognition_score.append(nlp_cognition.similarity(nlp_tweet))
            affection_score.append(nlp_affection.similarity(nlp_tweet))

        # record the affection score and cognition score to df
        df['affection'] = affection_score
        df['cognition'] = cognition_score

        # record the smoothened affection:cognition score ratio to df
        df['ratio'] = (df['affection'] + 1) / (df['cognition'] + 1)
        return df

    def calculate_num_token(self, df):
        # number of tokens used CHANGE IF INCLUDE HASHTAG
        num_token = []
        for i in range(len(df['Tweet'])):
            nlp_tweet = nlp(self.preprocess_text(df['Tweet'][i]))
            num_token.append(len(nlp_tweet))

        # record the number of tokens to df
        df['token'] = num_token
        return df

    def detect_lang(self, df):
        # computes the language of the tweet using package langdetect
        language = []
        for i in range(len(df['Tweet'])):
            if self.preprocess_text(df['Tweet'][i]) != '':
                language.append(detect(self.preprocess_text(df['Tweet'][i])))
            else:
                language.append('en')

        # record the language to df
        df['language'] = language
        return df

    def detect_hashtag(self, df):
        # in each tweet, find all hashtags
        hashtags = []
        for i in range(len(df['Tweet'])):
            hashtags.append(" ".join(re.findall("#(\w+)", df['Tweet'][i])))

        # record hashtags to df
        df['hashtags'] = hashtags
        return df

    def detect_num_hashtag(self, df):
        # in each tweet, record the number of hashtags
        hashtags_length = []
        for i in range(len(df['Tweet'])):
            hashtags_length.append(len(re.findall("#(\w+)", df['Tweet'][i])))

        # record the number of hashtags to df
        df['hashtags_length'] = hashtags_length
        return df

    def calculate_all(self):
        df = load_data(self.data_path)
        df = self.calculate_score(df)
        df = self.calculate_num_token(df)
        df = self.detect_lang(df)
        df = self.detect_hashtag(df)
        df = self.detect_num_hashtag(df)
        return df

    def sample_emotional_tweets(self, df, most_emotional:bool = True):
        # for each party, compute its most emotional tweets randomly chosen 10 from top 5%
        # chosen from those with at least 4 tokens (otherwise, too little context)
        # and only English tweets
        # REQUIRE df to have column "Party"
        df = self.calculate_all(df)
        sample_tweet = dict(list)

        if "Party" not in df.columns():
            raise Exception("df must have column Party!")

        for party in df["Party"].unique():
            filtered_df = df[(df['language'] == 'en') & (df['token'] > 4) & (df['Party'] == party)].sort_values('ratio', ascending = False)
            all_tweet = filtered_df.head(int(len(df)*(5/100)))['Tweet'] if most_emotional else filtered_df.tail(int(len(df)*(5/100)))['Tweet']
            sample = random.sample(list(all_tweet), 10)
            sample_tweet[party] = sample
        return pd.DataFrame(sample_tweet)

    def odd_ratio_hashtag_party(self, df, party:str):
        # for each party, compute its most emotional tweets randomly chosen 10 from top 5%
        # chosen from those with at least 4 tokens (otherwise, too little context)
        # and only English tweets
        # REQUIRE df to have column "Party"
        df = self.calculate_all(df)
        df = df[(df['language'] == 'en') & (df['token'] > 4)].sort_values('ratio', ascending = False)
        num = (1 + sum(pd.Series(df['hashtags']).str.contains(hashtag)))
        den = len(df['hashtags'])

        if "Party" not in df.columns():
            raise Exception("df must have column Party!")
        if party not in df["Party"].unique():
            raise Exception("this party", party, "is not in the column Party!")

        filtered_df = df[(df['language'] == 'en') & (df['token'] > 4) & (df['Party'] == party)].sort_values('ratio', ascending = False)
        num_filtered = (1 + sum(pd.Series(filtered_df['hashtags']).str.contains(hashtag)))
        den_filtered = len(filtered_df["hashtags"])

        odd_ratio = []
        hashtags = list(df["hashtags"])

        # compute the odd-ratio for this party with affection:cognition ratios against other types of hashtags
        for hashtag in hashtags:
            try:
                p = num_filtered / den_filtered
                q = (num - num_filtered) / (den - den_filtered)
                odd_ratio.append((p/(1 - p))/(q/(1 - q)))
            except:
                odd_ratio.append(-1)

        return pd.DataFrame({"hashtag": hashtags, "odd_ratio": odd_ratio}).sort_values('odd_ratio', ascending = False)['hashtag']