from langdetect import detect
import nltk 
nltk.download('stopwords')
from nltk.corpus import stopwords
import pandas as pd
import preprocessor as p
import random
import re
import spacy

from emotion-twitter import EmotionMeter

meter = EmotionMeter(data_path = "ExtractedTweets.csv")

print(meter.sample_emotional_tweets(most_emotional = True)) # print sample most emotional tweets
print(meter.odd_ratio_hashtag_party(party = "Republican")) # print odd ratio per hashtag in Republican's tweets
