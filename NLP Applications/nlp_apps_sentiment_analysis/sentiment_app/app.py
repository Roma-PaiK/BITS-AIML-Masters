from flask import Flask, render_template, request
from model import predict_sentiment
import io

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    result = None
    user_text = ""

    if request.method == "POST":
        # Check if a file was uploaded
        if 'file' in request.files and request.files['file'].filename != '':
            file = request.files['file']
            user_text = file.read().decode('utf-8')
        # Otherwise, get text from the textarea
        elif "text" in request.form:
            user_text = request.form["text"]

        if user_text:
            label, scores = predict_sentiment(user_text)

            # confidence
            confidence = round(abs(scores["compound"]) * 100, 2)

            # emoji mapping
            emoji_map = {
                "Positive": "😊",
                "Neutral": "😐",
                "Negative": "😡"
            }

            # message logic
            if label == "Positive":
                msg = "Great! Customers seem happy."
            elif label == "Negative":
                msg = "Alert: Customer dissatisfaction detected."
            else:
                msg = "Neutral feedback. Could improve."

            result = {
                "label": label,
                "emoji": emoji_map[label],
                "confidence": confidence,
                "scores": scores,
                "message": msg,
                "text": user_text
            }

    return render_template("index.html", result=result)


if __name__ == "__main__":
    app.run(debug=True)
