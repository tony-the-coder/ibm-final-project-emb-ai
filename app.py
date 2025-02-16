"""
This is a final project for the IBM AI Developer Professional Certificate course
"""


import json
import requests
from flask import Flask, render_template, request, jsonify
from EmotionDetection.emotion_detection import emotion_detector as emotion_detection



app = Flask(__name__)



@app.route('/')
def index():
    """Renders the index.html template."""
    return render_template('index.html')



@app.route('/emotionDetector', methods=['GET', 'POST'])
def analyze_emotion():
    """
    Analyzes the emotion of the provided text.
    """
    if request.method == 'POST':
        text_to_analyze = request.form.get('textToAnalyze')
    elif request.method == 'GET':
        text_to_analyze = request.args.get('textToAnalyze')
    else:
        return jsonify({"error": "Invalid request method"}), 400

    if not text_to_analyze:
        return jsonify({"error": "No text provided"}), 400

    try:
        response = emotion_detection(text_to_analyze)
        json_response = json.loads(response)

        if "error" in json_response:
            return jsonify(json_response), 400

        emotions = {k: v for k, v in json_response.items() if k!= 'dominant_emotion'}
        dominant_emotion = json_response.get('dominant_emotion')

        if dominant_emotion is None:
            return jsonify({"error": "Invalid text! Please try again!"}), 200

        output_string = f"Dominant Emotion: {dominant_emotion}<br>Emotions:<br>"
        for emotion, score in emotions.items():
            output_string += f"{emotion}: {score}<br>"

        return jsonify({"result": output_string}), 200

    # except Exception as e:
    #     return jsonify({"error": str(e)}), 500

    except requests.exceptions.RequestException as e:
        print(f"Request Error: {e}")
        return json.dumps({"error": str(e)})
