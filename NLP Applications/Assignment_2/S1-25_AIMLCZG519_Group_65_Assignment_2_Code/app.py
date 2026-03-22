from flask import Flask, render_template, request
from model import predict_sentence
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
            label, confidence, scores = predict_sentence(user_text)

            # emoji mapping
            emoji_map = {
                "positive": "😊",
                "neutral": "😐",
                "negative": "😡"
            }

            # message logic
            if label == "positive":
                msg = "Great! Customers seem happy."
            elif label == "negative":
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
