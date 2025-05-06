# app.py
from flask import Flask, request, jsonify
import cv2
import numpy as np
import os
from detect_cards import load_templates, find_cards
from werkzeug.utils import secure_filename

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

templates = load_templates()

@app.route("/detect", methods=["POST"])
def detect_cards():
    if "image" not in request.files:
        return jsonify({"error": "No image uploaded"}), 400

    file = request.files["image"]
    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

    image = cv2.imread(filepath)
    detected_cards = find_cards(image, templates)

    # Suodata parhaat osumat per kortti
    unique = {}
    for card, pt, score in detected_cards:
        if card not in unique or score > unique[card][1]:
            unique[card] = (pt, score)

    results = [card for card in unique.keys()]
    return jsonify({"cards": results})

if __name__ == "__main__":
    app.run(debug=True)