"""
app.py — Flask API for the prompt injection detector.
Runs both rule-based and ML detection on submitted text.
"""

from flask import Flask, jsonify, render_template, request

from detector import get_verdict
from ml_classifier import model, vectorizer

app = Flask(__name__)


@app.route("/analyze", methods=["POST"])
def analyze():
    """
    Receive text, run both detectors, and return the results.
    """
    data = request.get_json()
    text = data.get("text")

    if not text:
        return jsonify({"error": "No text provided"}), 400

    # Rule-based detector
    rule_result = get_verdict(text)

    # ML detector
    text_vectorized = vectorizer.transform([text])
    ml_prediction = model.predict(text_vectorized)[0]
    ml_confidence = model.predict_proba(text_vectorized)[0]

    result = {
        "text": text,
        "rule_based": {
            "is_injection": rule_result["is_injection"],
            "confidence": rule_result["confidence"],
            "rules_fired": rule_result["matches"],
        },
        "ml_classifier": {
            "is_injection": bool(ml_prediction == 1),
            "confidence_benign": round(float(ml_confidence[0]), 4),
            "confidence_injection": round(float(ml_confidence[1]), 4),
        },
    }

    return jsonify(result)


@app.route("/")
def home():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
