import nltk
import re

def lexical_diversity(text):
    return len(text) / len(set(text))

def plural(word):
    if word.endswith('y'):
        return word[:-1] + 'ies'
    elif word[-1] in 'sx' or word[-2:] in ['sh', 'ch']:
        return word + 'es'
    elif word.endswith('an'):
        return word[:-2] + 'en'
    else:
        return word + 's'

def unusual_words(text):
    text_vocab = set(w.lower() for w in text if w.isalpha())
    english_vocab = set(w.lower() for w in nltk.corpus.words.words())
    unusual = text_vocab - english_vocab
    return sorted(unusual)

def content_fraction(text):
    stopwords = nltk.corpus.stopwords.words('english')
    content = [w for w in text if w.lower() not in stopwords]
    return len(content) / len(text)

def generate_model(cfd, word, num=15):
    for i in range(num):
        print(word, end=' ')
        word = cfd[word].max()


def stress(pron):
    return [char for phone in pron for char in phone if char.isdigit()] # whatever is in front of 1st FOR statement
                                                                        # is dded to the list

def compress(word):
    regexp = r'^[AEIOUaeiou]+|[AEIOUaeiou]+$|[^AEIOUaeiou]'
    pieces = re.findall(regexp, word)
    return ''.join(pieces)

def stem(word):
    regexp = r'(^.*?)(ly|ing|ed|ious|ies|ive|es|s|ment)?$'
    stem, suffix = re.findall(regexp, word)[0]
    return stem

def tabulate(cfdist, words, categories, width_cat, width_event):                              # dynamic column width: 'max(len(x) for w in words)'
    print('{:{width_cat}}'.format('Category', width_cat=width_cat), end=' ')                  # column headings
    for x in words:
        print('{:>{width_event}}'.format(x, width_event=width_event), end=' ')
    print()
    for x in categories:
        print('{:{width_cat}}'.format(x, width_cat=width_cat), end=' ')                       # row heading
        for y in words:                                                                       # for each word
            print('{:{width_event}}'.format(cfdist[x][y], width_event=width_event), end=' ')  # print table cell
        print()    

wordlist = nltk.corpus.words.words()
stopwords = nltk.corpus.stopwords.words('russian')