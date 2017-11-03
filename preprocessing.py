import re
import string

from nltk import PorterStemmer
from nltk import SnowballStemmer
from nltk.corpus import stopwords
from nltk.stem.lancaster import LancasterStemmer
from nltk.tokenize import word_tokenize, sent_tokenize


def tokenize(text):
    return [word_tokenize(" ".join(re.findall(r'\w+', t, flags=re.UNICODE)).lower())
            for t in sent_tokenize(text.replace("'", ""))]


def check_if_word(word):
    for ch in word.lower():
        if ch not in string.ascii_lowercase:
            return False
    return True


def remove_stopwords(l_words, lang='english'):
    l_stopwords = stopwords.words(lang)
    content = [w for w in l_words if w.lower() not in l_stopwords and len(w) > 2 and check_if_word(w)]
    return content


def stemming(words_l, stem_type="PorterStemmer", lang="english", encoding="utf8"):
    supported_stemmers = ["PorterStemmer", "SnowballStemmer", "LancasterStemmer", "WordNetLemmatizer"]
    if stem_type is False or stem_type not in supported_stemmers:
        return words_l
    else:
        l = []
        if stem_type == "PorterStemmer":
            stemmer = PorterStemmer()
            for word in words_l:
                l.append(stemmer.stem(word).encode(encoding))
        if stem_type == "SnowballStemmer":
            stemmer = SnowballStemmer(lang)
            for word in words_l:
                l.append(stemmer.stem(word).encode(encoding))
        if stem_type == "LancasterStemmer":
            stemmer = LancasterStemmer()
            for word in words_l:
                l.append(stemmer.stem(word).encode(encoding))
        return l


def preprocess_pipeline(text, lang="english", stemmer_type="PorterStemmer"):
    l = []
    sentences = tokenize(text)
    for sentence in sentences:
        l += stemming(remove_stopwords(sentence, lang), stemmer_type)
    return l
