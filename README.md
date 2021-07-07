# emotionmeter
Python code for producing emotionality scores from Gennaro and Ash (2021).

To set up,

- Type `pip install -r requirements.txt` in command line to install dependency packages (or pip3 in some systems e.g. Ubuntu)
- Type `python3 -m spacy download en_core_web_lg` in command line to install necessary language corpus for package `spacy`

and

- Put the .csv file that contains your dataset in folder `data`

To use, 
- see `main.py` for example usage, e.g.:

```
from emotionmeter import EmotionMeter

meter = EmotionMeter(data_path="data/ExtractedTweets.csv", text_column="Tweet")

meter_with_score = meter.calculate_all() # get df with calculated reasoning and emotional scores
print(meter.sample_emotional_tweets(most_emotional = True)) # print sample most emotional tweets
print(meter.odd_ratio_hashtag_party(party = "Republican")) # print odd ratio per hashtag in Republican's tweets
```
If you would like to import the package into your own script outside the package folder, change the directory in the import part `from ... import ...` on the first line. Also change the `data_path` if your data is saved somewhere else other than `/data`
