#### Python 3.9.6 !!!

import re
from pathlib import Path

import joblib
from pymorphy2 import MorphAnalyzer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

BASE_DIR = Path(__file__).parent.resolve()


def load(filename):
    path = BASE_DIR.joinpath(filename)
    return joblib.load(path)


TOKEN_RE = re.compile(r'[а-яё]+')
keywords: dict = load('src/keywords.pkl')

russian_stopwords = set(keywords.get('stopwords', []))
swearings = set(keywords.get('swear', []))


class ModerationService:
    lemmatizer = MorphAnalyzer()

    model: LogisticRegression = load('src/Logregres.pkl')
    vectorizer: TfidfVectorizer = load('src/Vectorizer.pkl')

    def tokenize_text(self, txt: str, min_lenght_token=2):
        txt = str(txt).lower()
        all_tokens = TOKEN_RE.findall(txt)
        return [token for token in all_tokens if len(token) >= min_lenght_token]

    def lemmatizing(self, tokens):
        return [self.lemmatizer.parse(token)[0].normal_form for token in tokens]

    def remove_stopwords(self, tokens):
        return list(filter(lambda token: token not in russian_stopwords, tokens))

    def clean_text(self, txt: str):
        tokens = self.tokenize_text(txt)
        tokens = self.lemmatizing(tokens)
        tokens = self.remove_stopwords(tokens)
        return ' '.join(tokens)

    def validate(self, text: str):
        tokens = self.tokenize_text(text)

        text_swearings = set(tokens) & swearings

        print('tokenize_text =', tokens)

        if text_swearings:
            return 1

        tokens = self.lemmatizing(tokens)

        print('lemmatizing =', tokens)

        tokens = self.remove_stopwords(tokens)

        print('remove_stopwords =', tokens)

        cleaned_text = ' '.join(tokens)

        if not cleaned_text.strip():
            return 0

        X_example = self.vectorizer.transform([cleaned_text])
        toxic_propabality = self.model.predict_proba(X_example)[0, 1]

        return toxic_propabality
    

if __name__ == '__main__':
    service = ModerationService()
    service.validate('....')