from flask import Flask, render_template, request, jsonify
import joblib

# Load Model
model = joblib.load("mental_health_model.pkl")
vectorizer = joblib.load("tfidf_vectorizer.pkl")

app = Flask(__name__)

# Serve the HTML page
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    try:
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
    app.run(debug=False,host='0.0.0.0')
