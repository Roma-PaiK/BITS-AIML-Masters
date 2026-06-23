import re
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize

nltk.download('vader_lexicon')
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('omw-1.4')

sia = SentimentIntensityAnalyzer()
lemmatizer = WordNetLemmatizer()

def preprocess(text):
    # 1. Lowercase and remove special characters
    text = text.lower()
    text = re.sub(r'[^a-zA-Z ]', '', text)
    
    # 2. Tokenization (Requirement 2.2)
    tokens = word_tokenize(text)
    
    # 3. Lemmatization (Requirement 2.2)
    # Reduces words to their base form for better analysis
    lemmatized_text = [lemmatizer.lemmatize(word) for word in tokens]
    
    return " ".join(lemmatized_text)

def predict_sentiment(text):
    clean_text = preprocess(text)
    print(f"Preprocessed Text: {clean_text}")
    score = sia.polarity_scores(clean_text)

    # Sentiment Prediction Logic (Requirement 2.3)
    if score['compound'] >= 0.05:
        label = "Positive"
    elif score['compound'] <= -0.05:
        label = "Negative"
    else:
        label = "Neutral"

    print(f"Sentiment Scores: {score}")
    print(f"Predicted Sentiment: {label}")

    return label, score
