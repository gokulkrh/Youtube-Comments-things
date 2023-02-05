import joblib
from Preprocess import prep_comments
from sklearn.linear_model import SGDClassifier


def spam_or_ham(comment):
    model = joblib.load('Spam_Filter/Spam_classifier_1.pkl')
    comment = prep_comments.vectorized_comment(comment)
    return model.predict(comment)
