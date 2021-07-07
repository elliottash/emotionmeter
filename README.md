# emotionmeter
Python code for producing emotionality scores from Gennaro and Ash (2021).

To set up,

- type `pip install -r requirements.txt` in command line to install dependency packages (or pip3 in some systems e.g. Ubuntu)
- type `python3 -m spacy download en_core_web_lg` in command line to install necessary language corpus for package `spacy`

and

- put the .csv file that contains your dataset in folder `data`. You may try with [our dataset](https://polybox.ethz.ch/index.php/s/Us2HeNYzsu509dm).

To use, 
- import the package `EmotionMeter` and create the instance of it, specifying `data_path` and `text_column`
- see `main.py` for example usage, e.g.:

```
from emotionmeter import EmotionMeter

meter = EmotionMeter(data_path="data/ExtractedTweets.csv", text_column="Tweet")

meter_with_score = meter.calculate_all() # get df with calculated reasoning and emotional scores
print(meter.sample_emotional_tweets(most_emotional = True)) # print sample most emotional tweets
print(meter.odd_ratio_hashtag_party(party = "Republican")) # print odd ratio per hashtag in Republican's tweets
```

- If you would like to import the package into your own script outside the package folder, change the directory in the import part `from ... import EmotionMeter` on the first line
- Also change the `data_path` if your data is saved somewhere else other than `/data`
