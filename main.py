
from emotionmeter import EmotionMeter

meter = EmotionMeter(data_path = "data/ExtractedTweets.csv")

print(meter.sample_emotional_tweets(most_emotional = True)) # print sample most emotional tweets
print(meter.odd_ratio_hashtag_party(party = "Republican")) # print odd ratio per hashtag in Republican's tweets
