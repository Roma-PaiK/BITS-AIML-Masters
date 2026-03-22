# Sentiment Analysis Web Application

A Flask-based NLP web application that performs **Sentiment Analysis** using a trained Voting Ensemble classifier.

The model was trained using multiple machine learning algorithms and deployed through a simple web interface.

---

## Team Contribution

| Name of Student     | BITS ID                              | Contribution |
|---------------------|----------------------------------------|-------------|
| K ROMA PAI          | 2024aa05965@wilp.bits-pilani.ac.in    | 100%        |
| JITESH GUPTA        | 2024ab05020@wilp.bits-pilani.ac.in    | 100%        |
| KOTHA AMITABH       | 2024ab05195@wilp.bits-pilani.ac.in    | 100%        |
| JOHIT GARG          | 2024aa05907@wilp.bits-pilani.ac.in    | 100%        |
| KARTHIK REDDY S     | 2024ab05330@wilp.bits-pilani.ac.in    | 100%        |

---

## Project Structure

```
sentiment_app/
│
├── app.py                  # Main Flask application
├── model.py                # Loads trained model & handles predictions
├── requirements.txt        # Required Python packages
├── sample_text.txt         # Sample input text file
│
├── models/                 # Saved trained models
│   ├── ensemble_model.pkl
│   └── vectorizer.pkl
│
├── templates/              # HTML template for Flask
│   └── index.html
│
└── training/               # Model training notebook
    ├── S1_25_AIMLCZG519_Group_65_Assignment_2_Training_Code.ipynb
    └── S1_25_AIMLCZG519_Group_65_Assignment_2_Training_Code.pdf # ipynb notebook pdf export
```

---

## Features

- Text preprocessing using:
  - Tokenization
  - Stopword removal
  - Lemmatization
  - Stemming
- TF-IDF Vectorization
- Soft Voting Ensemble Model
- Web-based prediction interface
- Confidence score display (probabilistic predictions)

---

## Model Details

The final model is a **Soft Voting Ensemble Classifier** built using:

- Logistic Regression  
- Support Vector Machine (with probability enabled)  
- Naive Bayes  
- SGD Classifier  
- Decision Tree  
- Random Forest  

The ensemble combines predictions using weighted soft voting.

---

## Technologies Used

- Python
- Flask
- scikit-learn
- NLTK
- NumPy
- Pandas

---

## Installation

1. Download the project folder.

2. Navigate to the project directory:

```bash
cd sentiment_app
```

3. Create a virtual environment: (Optional but recommended)

```bash
python -m venv venv
venv\Scripts\activate
```

4. Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Running the Application

Run the Flask app:

```bash
python app.py
```

Open your browser and visit:

```
http://127.0.0.1:5000/
```

---

## NLTK Resources

The application downloads the following NLTK datasets at runtime:

- punkt
- wordnet
- stopwords

If running in an environment without internet access, download them manually before deployment.

---

## Training Details

- Model training was performed in Google Colab.
- The training notebook is available inside the `training/` folder.
- The final trained ensemble model and TF-IDF vectorizer are stored in the `models/` directory.
- The final ensemble model size is approximately 26MB.

---

## Example Input

You can test the application using text from:

```
sample_text.txt
```

---

## Objective

This project demonstrates:

- Text preprocessing in NLP
- Feature engineering using TF-IDF
- Ensemble learning techniques
- Deployment of ML models using Flask

---

