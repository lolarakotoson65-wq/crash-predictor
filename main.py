from flask import Flask, request, jsonify
import numpy as np

app = Flask(__name__)

def analyze(data):
    data = np.array(data)

    mean = np.mean(data)
    variance = np.var(data)

    low = np.sum(data < 1.5)
    high = np.sum(data > 3)

    risk_score = (low * 2 + variance) - high

    if risk_score > 10:
        return "DANGEREUX", "attendre"
    elif risk_score > 5:
        return "INSTABLE", "jouer petit (1.5x)"
    else:
        return "SAFE", "jouer normal (2x)"

@app.route("/predict", methods=["POST"])
def predict():
    data = request.json.get("history", [])

    if len(data) < 5:
        return jsonify({"error": "pas assez de données"})

    state, advice = analyze(data)

    return jsonify({
        "etat": state,
        "conseil": advice
    })

@app.route("/")
def home():
    return "Serveur analyse crash OK"

if __name__ == "__main__":
    app.run()
