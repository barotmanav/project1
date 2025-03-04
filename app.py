from flask import Flask, render_template, request, jsonify
import joblib
import os

# Initialize Flask app
app = Flask(__name__)

# Load Model & Vectorizer (Check if files exist)
model_path = "mental_health_model.pkl"
vectorizer_path = "tfidf_vectorizer.pkl"

if os.path.exists(model_path) and os.path.exists(vectorizer_path):
    model = joblib.load(model_path)
    vectorizer = joblib.load(vectorizer_path)
else:
    model, vectorizer = None, None

# Serve the HTML page
@app.route("/")
def home():
    if os.path.exists("templates/index.html"):
        return render_template("index.html")
    return "index.html not found. Please add it to the templates folder.", 500

# Prediction Route
@app.route("/predict", methods=["POST"])
def predict():
    try:
        if model is None or vectorizer is None:
            return jsonify({"error": "Model files not found"}), 500

        data = request.json
        text = data.get("statement", "")

        if not text:
            return jsonify({"error": "No statement provided"}), 400

        # Transform text using TF-IDF vectorizer
        text_tfidf = vectorizer.transform([text])

        # Predict using the model
        prediction = model.predict(text_tfidf)[0]

        return jsonify({"prediction": prediction})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)  # Render requires this format
