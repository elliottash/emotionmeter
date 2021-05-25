# emotionmeter
Python code for producing emotionality scores from Gennaro and Ash (2021).

To set up,

- install dependency packages by typing `pip install -r requirements.txt` in command line

-- see `main.py` for example usage, e.g.:

```
from emotion-twitter import EmotionMeter

meter = EmotionMeter(data_path = "ExtractedTweets.csv")

print(meter.sample_emotional_tweets(most_emotional = True)) # print sample most emotional tweets
print(meter.odd_ratio_hashtag_party(party = "Republican")) # print odd ratio per hashtag in Republican's tweets
```
