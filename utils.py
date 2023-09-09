

import pickle
from sklearn.base import BaseEstimator, TransformerMixin
from underthesea import word_tokenize
import urllib.parse


with open('tfidf_vectorizer.pkl', 'rb') as f:
    vectorizer = pickle.load(f)
class ProcessText(BaseEstimator, TransformerMixin):
    def __init__(self):
        pass

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        if isinstance(X, list):
            return self.process(X)
        return self.process([X])
    def process(self, text):
        for t in text:
            t = t.lower()
            t = word_tokenize(t, format="text")
        return vectorizer.transform(text).toarray()
    
def get_dict_trans():
    return  {
    'giao-duc': 'Giáo dục',
    'the-thao': 'Thể thao',
    'khoa-hoc': 'Khoa học',
    'suc-khoe': 'Sức khỏe',
    'du-lich': 'Du lịch'
}
def is_url(text):
    try:
        result = urllib.parse.urlparse(text)
        return all([result.scheme, result.netloc])  # Kiểm tra xem có scheme và netloc hay không
    except ValueError:
        return False
    
def is_vnexpress_url(url):
    return url.startswith('https://vnexpress.net')