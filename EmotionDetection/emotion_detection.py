import requests
import json

def emotion_detector(text_to_analyze):
    url = 'https://sn-watson-emotion.labs.skills.network/v1/watson.runtime.nlp.v1/NlpService/EmotionPredict'
    myobj = {"raw_document": {"text": text_to_analyze}}
    header = {"grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"}

    if not text_to_analyze or text_to_analyze.strip() == "":  # Check for blank input FIRST
        return json.dumps({
            "anger": None,
            "disgust": None,
            "fear": None,
            "joy": None,
            "sadness": None,
            "dominant_emotion": None
        })

    try:
        response = requests.post(url, json=myobj, headers=header, timeout=10)
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)

        json_response = response.json()
        emotions = json_response['emotionPredictions']['emotionMentions']['emotion']
        dominant_emotion = max(emotions, key=emotions.get, default=None)
        emotion_response = {
            **emotions,
            'dominant_emotion': dominant_emotion
        }
        return json.dumps(emotion_response, indent=4)

    except requests.exceptions.RequestException as e:
        print(f"Request Error: {e}")
        return json.dumps({"error": str(e)})  # Return JSON error message

    except (KeyError, IndexError) as e:
        print(f"JSON Error: {e}")
        return json.dumps({"error": "Could not extract text from API response"})

    except Exception as e:
        print(f"Unexpected Error: {e}")
        return json.dumps({"error": "An unexpected error occurred"})