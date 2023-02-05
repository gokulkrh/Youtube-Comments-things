import string
import html
import re
import joblib
from sklearn.feature_extraction.text import CountVectorizer
from nltk.corpus import stopwords
from textblob import Word
import nltk
nltk.download('stopwords')
stop = stopwords.words('english')


def remove_html(raw_comment):
    raw_comment = html.unescape(raw_comment)
    raw_comment = "".join(x for x in raw_comment if x in string.printable)
    raw_comment = re.sub(r'<[^<]+?>', ' ', raw_comment)
    return raw_comment


def remove_links_tags(raw_comment):
    raw_comment = re.sub("@[A-Za-z0-9_]+", "", raw_comment)
    raw_comment = re.sub("#[A-Za-z0-9_]+", "", raw_comment)
    raw_comment = re.sub("^https?:\/\/.*[\r\n]*", "", raw_comment)
    return raw_comment


def remove_repeating_chars(raw_comment):
    pattern = re.compile(r"(.)\1{2,}")
    return pattern.sub(r"\1\1", raw_comment)


def remove_nps(raw_comment):
    raw_comment = re.sub('[^\w\s]', ' ', raw_comment)
    raw_comment = re.sub('[0-9]', ' ', raw_comment)
    return raw_comment


def remove_stw_lemmatize(raw_comment):
    raw_comment = " ".join(x for x in raw_comment.split() if x not in stop)
    raw_comment = " ".join([Word(word).lemmatize() for word in raw_comment.split()])
    return raw_comment


def cleaned_comment(raw_comment):
    raw_comment = remove_links_tags(raw_comment)
    raw_comment = remove_html(raw_comment)
    return raw_comment


def preprocessed_comment(raw_comment):
    raw_comment = cleaned_comment(raw_comment)
    raw_comment = remove_nps(raw_comment)
    raw_comment = remove_stw_lemmatize(raw_comment)
    raw_comment = remove_repeating_chars(raw_comment)
    raw_comment = raw_comment.lower()
    return raw_comment


def vectorized_comment(raw_comment):
    preprocessed_comment(raw_comment)
    vectorizer = joblib.load('Preprocess/count_vectorizer_1.pkl')
    comment_vector = vectorizer.transform([raw_comment])
    return comment_vector
