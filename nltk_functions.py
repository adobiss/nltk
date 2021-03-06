import nltk
import re
import math

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


def findtags(tags_prefix, tagged_text):
    cfd = nltk.ConditionalFreqDist((y, x) for x, y in tagged_text
                                   if y.startswith(tags_prefix))
    return dict((y, cfd[y].most_common(5)) for y in cfd.conditions())


def process(sentence):
    for (x1, y1), (x2, y2), (x3, y3) in nltk.trigrams(sentence):
        if(y1.startswith('V') and y2 == 'TO' and y3.startswith('V')):
            print(x1, x2, x3)


def performance(cfd, wordlist, tag_sents):
    likely_tags = dict((x, cfd[x].max()) for x in wordlist)
    baseline_tagger = nltk.UnigramTagger(model=likely_tags,
                                         backoff=nltk.DefaultTagger('NN'))
    return baseline_tagger.evaluate(tag_sents)


def display(most_common_words, tagged_words, tag_sents):
    import pylab
    word_freqs = most_common_words
    words_by_freq = [x for x, y in word_freqs]
    cfd = nltk.ConditionalFreqDist(tagged_words)
    sizes = 2 ** pylab.arange(15)
    perfs = [performance(cfd, words_by_freq[:x], tag_sents) for x in sizes]
    pylab.plot(sizes, perfs, '-bo')
    pylab.title('Lookup Tagger Performance with Varying Model Size')
    pylab.xlabel('Model Size')
    pylab.ylabel('Performance')
    pylab.show()


def gender_features(name):
    return {'suffix1': name[-1],
            'suffix2': name[-2:]}


def gender_features2(name):
    features = {}
    features['first_letter'] = name[0].lower()
    features['last_letter'] = name[-1].lower()
    for x in 'abcdefghijklmnopqrstuvwxyz':
        features['count({})'.format(x)] = name.lower().count(x)
        features['has({})'.format(x)] = (x in name.lower())
    return features


def entropy(labels):
    freqdist = nltk.FreqDist(labels)
    probs = [freqdist.freq(x) for x in freqdist]
    return -sum(x * math.log(x,2) for x in probs)


def document_features(document, all_words, word_features):
    document_words = set(document) # checking an 'IF x in y' statement is faster in a set than in a list
    features = {}
    for x in word_features:
        features['contains({})'.format(x)] = (x in document_words)
    return features


# Context-dependant feature extractor:  
    
def pos_features_context(sentence, i):
    features = {"suffix(1)": sentence[i][-1:],
                "suffix(2)": sentence[i][-2:],
                "suffix(3)": sentence[i][-3:]}
    if i == 0:
        features["prev-word"] = "<START>"
    else:
        features["prev-word"] = sentence[i-1]
    return features


# Uses pos_features_context() to build featuresets
# (requires review to work in conjunction with apply_features()):
    
def featureset_buider(tagged_sents):
    featuresets = []
    for x in tagged_sents:
        untagged_sent = nltk.tag.untag(x)
        for i, (word, tag) in enumerate(x):
            featuresets.append( (pos_features_context(untagged_sent, i), tag) ) 


         
# Return all phrase chunks from corpus that match certain tag pattern:   
    
def find_chunks(grammar, tagged_sents):
    cp = nltk.RegexpParser(grammar)
    for x in tagged_sents:
        tree = cp.parse(x)
        for y in tree.subtrees():
            if y.label() == grammar.split(':')[0]: print(y)
            
            
                                         
wordlist = nltk.corpus.words.words()
stopwords = nltk.corpus.stopwords.words('russian')