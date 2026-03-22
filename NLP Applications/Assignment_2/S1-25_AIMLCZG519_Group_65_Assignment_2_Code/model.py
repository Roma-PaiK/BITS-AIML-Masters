import re
import pickle
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer, PorterStemmer
from nltk.tokenize import word_tokenize
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


nltk.download('punkt', quiet=True)
nltk.download('wordnet', quiet=True)
nltk.download('stopwords', quiet=True)

lemmatizer = WordNetLemmatizer()
stemmer = PorterStemmer()
stop_words = set(stopwords.words('english'))

# Load the saved model and vectorizer
model_path = os.path.join(BASE_DIR, "models", "ensemble_model.pkl")
vectorizer_path = os.path.join(BASE_DIR, "models", "tfidf_vectorizer.pkl")


model = pickle.load(open(model_path, "rb"))
vectorizer = pickle.load(open(vectorizer_path, "rb"))

def preprocess_text(text):
    text = text.lower()
    text = re.sub(r'[^a-zA-Z ]', '', text)

    tokens = word_tokenize(text)
    processed_tokens = []

    for word in tokens:
        if word not in stop_words:
            lemma = lemmatizer.lemmatize(word)
            stem = stemmer.stem(lemma)
            processed_tokens.append(stem)

    return " ".join(processed_tokens)

def predict_sentence(sentence):
    """
    Processes a sentence and returns:
    - prediction
    - confidence (%)
    - full probability array
    """

    # Preprocess (using your existing function unchanged)
    clean_sentence = preprocess_text(sentence)

    # Vectorize
    vectorized_sentence = vectorizer.transform([clean_sentence])

    # Predict
    prediction = model.predict(vectorized_sentence)[0]

    # Probabilities
    probabilities = model.predict_proba(vectorized_sentence)[0]

    # Confidence (highest probability in %)
    confidence = round(max(probabilities) * 100, 2)

    return prediction, confidence, probabilities
