from nltk.corpus import genesis
from nltk_functions import lexical_diversity, plural, unusual_words, content_fraction
from nltk.corpus import gutenberg, nps_chat


kjv = genesis.words('english-kjv.txt')
text = gutenberg.words('austen-sense.txt')
chat = nps_chat.words()

#print(lexical_diversity(kjv))
#print(plural('woman'))
#print(unusual_words(chat)[:20])
print(content_fraction(text))