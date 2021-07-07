
f = open('cognition_list.txt','r')
cognition_list = f.read().split('\n')
f.close() 

f = open('affect_list.txt','r')
affection_list = f.read().split('\n')
f.close()

cog = list(set(cognition_list))
aff = list(set(affection_list))

import nltk 
nltk.download('stopwords')
from nltk.corpus import stopwords

stop = set(stopwords.words("english"))

cog = [c for c in cog if c not in stop]
aff = [c for c in aff if c not in stop]