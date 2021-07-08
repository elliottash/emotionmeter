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
    def __init__(self, 
            data_path:str = "data/smallExtractedTweets.csv", 
            text_column:str = "Tweet", 
            corpus:str = "en_core_web_lg", 
            affection_path:str = "word_lists/affect_list.txt", 
            cognition_path:str = "word_lists/cognition_list.txt"
            ):
        self.data_path = data_path
        self.text_column = text_column
        self.affection_path = affection_path
        self.cognition_path = cognition_path
        self.load_cognition_and_cognition_word_lists()
        self.load_corpus(corpus)

    def load_cognition_and_cognition_word_lists(self):
        with open(self.affection_path, "r") as f:
            affect_list = f.readlines()
        self.aff = [word.strip() for word in affect_list]
        with open(self.cognition_path, "r") as f:
            cognition_list = f.readlines()
        self.cogg = [word.strip() for word in cognition_list]


    def load_corpus(self, corpus:str):
        corpus_prefix = corpus[:-3]
        try:
            self.nlp = spacy.load(f"{corpus_prefix}_lg")
            return
        except:
            print("large-sized corpus not available, trying medium one...")
            pass
        try:
            self.nlp = spacy.load(f"{corpus_prefix}_md")
            return
        except:
            print("medium-sized corpus not available, trying small one...")
            pass
        try:
            self.nlp = spacy.load(f"{corpus_prefix}_sm")
            return
        except:
            print("no corpus not available... try again")
            raise ValueError(f"no corpus {corpus_prefix}")

    @staticmethod
    def load_data(data_path, text_column:str = "Tweet"):
        # import tweet data from .csv
        # texts contain tweets on "Tweet" column!
        df = pd.read_csv(data_path)
        if text_column not in df.columns:
            raise Exception("df must have column "+text_column)
        else:
            df.columns = [text_column if (col == text_column) else col for col in df.columns]
        return df

    @staticmethod
    def preprocess_text(tweet, keep_hashtag_text:bool = False):
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
        cognition_list = self.cog
        affect_list = self.aff

        # cognition and affection scores CHANGE IF INCLUDE HASHTAG
        cognition_score = []
        affection_score = []

        nlp_cognition = self.nlp(' '.join(cognition_list))
        nlp_affection = self.nlp(' '.join(affect_list))

        # for each tweet, record its word vector's similarity to (average) cognition vector
        for i in range(len(df[self.text_column])):
            nlp_tweet = self.nlp(self.preprocess_text(df[self.text_column][i]))
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
        for i in range(len(df[self.text_column])):
            nlp_tweet = self.nlp(self.preprocess_text(df[self.text_column][i]))
            num_token.append(len(nlp_tweet))

        # record the number of tokens to df
        df['token'] = num_token
        return df

    def detect_lang(self, df):
        # computes the language of the tweet using package langdetect
        language = []
        for i in range(len(df[self.text_column])):
            if self.preprocess_text(df[self.text_column][i]) != '':
                language.append(detect(self.preprocess_text(df[self.text_column][i])))
            else:
                language.append('en')

        # record the language to df
        df['language'] = language
        return df

    def detect_hashtag(self, df):
        # in each tweet, find all hashtags
        hashtags = []
        for i in range(len(df[self.text_column])):
            hashtags.append(" ".join(re.findall("#(\w+)", df[self.text_column][i])))

        # record hashtags to df
        df['hashtags'] = hashtags
        return df

    def detect_num_hashtag(self, df):
        # in each tweet, record the number of hashtags
        hashtags_length = []
        for i in range(len(df[self.text_column])):
            hashtags_length.append(len(re.findall("#(\w+)", df[self.text_column][i])))

        # record the number of hashtags to df
        df['hashtags_length'] = hashtags_length
        return df

    def calculate_score_and_other_stats(self):
        df = self.load_data(self.data_path, text_column=self.text_column)
        df = self.calculate_score(df)
        df = self.calculate_num_token(df)
        df = self.detect_lang(df)
        df = self.detect_hashtag(df)
        df = self.detect_num_hashtag(df)
        return df

    def show_sample_emotional_tweets(self, from_most_emotional:bool = True, num_sample:int = 10, party:str = None):
        # for each party, compute its most emotional tweets randomly chosen 10 from top 5%
        # chosen from those with at least 4 tokens (otherwise, too little context)
        # and only English tweets
        # REQUIRE df to have column "Party"
        df = self.calculate_score_and_other_stats()
        sample_tweet = dict()

        filtered_df = df[(df['language'] == 'en') & (df['token'] > 4)].sort_values('ratio', ascending=False)
        if party is not None:
            if "Party" in filtered_df.columns:
                filtered_df = filtered_df[filtered_df["Party"] == party]
            else:
                raise Exception("df must have column Party!")
        all_tweet = filtered_df.head(int(len(df)*(5/100)))[self.text_column] if from_most_emotional else filtered_df.tail(int(len(df)*(5/100)))[self.text_column]
        num_sample = num_sample if len(all_tweet) >= num_sample else len(all_tweet)
        sample = random.sample(list(all_tweet), num_sample)
        return pd.DataFrame(sample)

    def show_hashtags_sorted_by_odd_for_party(self, party:str):
        # for each party, compute its most emotional tweets randomly chosen 10 from top 5%
        # chosen from those with at least 4 tokens (otherwise, too little context)
        # and only English tweets
        # REQUIRE df to have column "Party"
        df = self.calculate_score_and_other_stats()
        df = df[(df['language'] == 'en') & (df['token'] > 4)].sort_values('ratio', ascending=False)
        den = len(df['hashtags'])

        if "Party" not in df.columns:
            raise Exception("df must have column Party!")
        if party not in df["Party"].unique():
            raise Exception("this party", party, "is not in the column Party!")

        filtered_df = df[(df['language'] == 'en') & (df['token'] > 4) & (df['Party'] == party)].sort_values('ratio', ascending=False)
        den_filtered = len(filtered_df["hashtags"])

        odd_ratio = []
        hashtags = [hashtag for hashtag in list(df["hashtags"]) if hashtag.strip() != ""]

        # compute the odd-ratio for this party with affection:cognition ratios against other types of hashtags
        for hashtag in hashtags:
            num = (1 + sum(pd.Series(df['hashtags']).str.contains(hashtag)))
            num_filtered = (1 + sum(pd.Series(filtered_df['hashtags']).str.contains(hashtag)))
            try:
                p = num_filtered / den_filtered
                q = (num - num_filtered) / (den - den_filtered)
                odd_ratio.append((p/(1 - p))/(q/(1 - q)))
            except:
                odd_ratio.append(-1)

        return pd.DataFrame({"hashtag": hashtags, "odd_ratio": odd_ratio}).sort_values('odd_ratio', ascending=False)['hashtag']
