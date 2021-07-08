# emotionmeter
Python code for producing emotionality scores from Gennaro and Ash (2021).

To set up, from inside the main folder:

- type `pip install -r requirements.txt` in command line to install dependency packages (or pip3 in some systems e.g. Ubuntu)
- type `python -m spacy download en_core_web_sm` in command line to install the necessary language corpus for package `spacy` (or python3 in some systems). 
    - You may download other spacy-supported corpus in the format `{lang}_core_web_{size}` and specify it in `corpus` argument in the EmojionMeter initizalizer. You may check the list of supported languages with [spacy](https://spacy.io/usage/models#languages)

and

- put the .csv file that contains your dataset in folder `data`. You may try with [our dataset](https://polybox.ethz.ch/index.php/s/Us2HeNYzsu509dm).
- make sure the word lists `affect_list.txt` and `cognition_list.txt` are in folder `word_lists`. You may also use your own or ours that is already provided (or from the same [link](https://polybox.ethz.ch/index.php/s/Us2HeNYzsu509dm) if they are missing). 

To use, 
- import the package `EmotionMeter` and create the instance of it, specifying 
    - `data_path` for the path to your .csv data
    - `text_column` for the text column's name in the .csv
    - `corpus` in the format `{lang}_core_web_{size}`, where `size` could be `sm` for small, `md` for medium, or `lg` for large.
- see `main.py` for example usage, e.g.:

```
from emotionmeter import EmotionMeter # import the package

meter = EmotionMeter(data_path="data/smallExtractedTweets.csv", text_column="Tweet", corpus="en_core_web_sm") # and create the instance of it

meter_with_score = meter.calculate_score_and_other_stats() # get df with calculated reasoning and emotional scores
print(meter.show_sample_emotional_tweets(from_most_emotional=True)) # print sample most emotional tweets
print(meter.show_hashtags_sorted_by_odd_for_party(party="Democrat")) # print odd ratio per hashtag in Democrat's tweets
```

Some notes:
- If you would like to import the package into your own script outside the package folder, change the directory in the import part `from ... import EmotionMeter` on the first line
