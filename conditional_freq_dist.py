from nltk.probability import ConditionalFreqDist
from nltk.tokenize import word_tokenize
import nltk 
sent = "the the the dog dog some other words that we do not care about"
cfdist = ConditionalFreqDist()
for word in word_tokenize(sent):
    condition = len(word)
    cfdist[condition][word] += 1
    
cfdist.plot()