# emotionmeter
Python code for producing emotionality scores from Gennaro and Ash (2021).

To set up, from inside the main folder:

- type `pip install -r requirements.txt` in command line to install dependency packages (or pip3 in some systems e.g. Ubuntu)
- type `python -m spacy download en_core_web_sm` in command line to install the necessary language corpus for package `spacy` (or python3 in some systems). 
    - It is possible to use other spacy-supported corpus in the format `{lang}_core_web_{size}`, where `size` could be `sm` for small, `md` for medium, or `lg` for large. Make sure to download it (here) and specify it in `corpus` argument in the EmotionMeter initizalizer (see the example below). 
    - You may check the list of supported languages with [spacy](https://spacy.io/usage/models#languages)

and

- put the .csv file that contains your dataset in folder `data`. You may try with [our dataset](https://polybox.ethz.ch/index.php/s/Us2HeNYzsu509dm).
- make sure the word lists `affect_list.txt` and `cognition_list.txt` are in folder `word_lists`. You may also use your own or ours that is already provided (or from the same [link](https://polybox.ethz.ch/index.php/s/Us2HeNYzsu509dm) if they are missing). 

To use, 
- import the package `EmotionMeter` and create the instance of it, specifying 
    - `data_path` for the path to your .csv data, e.g. `"data/smallExtractedTweets.csv"`
    - `text_column` for the text column's name in the .csv, e.g. `"Tweet"`
    - `corpus` is the spaCy model for the pre-trained embeddings with format `{lang}_core_web_{size}`, e.g. `"en_core_web_sm"`
- for example usage, e.g.:

```
# import the package
from emotionmeter import EmotionMeter 

# and create the instance of it
meter = EmotionMeter(data_path="data/smallExtractedTweets.csv", 
                     text_column="Tweet", 
                     corpus="en_core_web_sm") 

# get df with calculated reasoning and emotional scores
meter_with_score = meter.calculate_score_and_other_stats() 

# print sample most emotional tweets
print(meter.show_sample_emotional_tweets(from_most_emotional=True)) 

# print odds ratio per hashtag in Democrat's tweets
print(meter.show_hashtags_sorted_by_odd_for_party(party="Democrat")) 
```

Some notes:
- If you would like to import the package into your own script outside the package folder, change the directory in the import part `from ... import EmotionMeter` on the first line
