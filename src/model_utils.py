

import pandas as pd
import numpy as np
import joblib
from transformers import pipeline
from src.nlp import extract_emotions


# cargar modelos una sola vez
model_valence = joblib.load("models/model_valence.pkl")
model_energy = joblib.load("models/model_energy.pkl")
model_mode = joblib.load("models/model_mode.pkl")
model_key = joblib.load("models/model_key.pkl")

feature_columns = joblib.load("models/features.pkl")


key_map = {
    0: "C", 1: "C#", 2: "D", 3: "D#", 4: "E", 5: "F",
    6: "F#", 7: "G", 8: "G#", 9: "A", 10: "A#", 11: "B"
}

def predict_song_profile(emotion_scores):

    X_input = pd.DataFrame([emotion_scores])

    #
    X_input = X_input.reindex(columns=feature_columns, fill_value=0)

    valence = model_valence.predict(X_input)[0]
    energy = model_energy.predict(X_input)[0]
    mode = model_mode.predict(X_input)[0]

    return {
        "valence": round(valence, 2),
        "energy": round(energy, 2),
        "mode": "major" if mode == 1 else "minor"
    }

def interpret_profile(valence, energy):
    if valence > 0.6 and energy > 0.6:
        return "Happy & Energetic"
    elif valence < 0.4 and energy < 0.4:
        return "Sad & Calm "
    elif energy > 0.6:
        return "Intense"
    else:
        return "Chill "
    
def predict_key(emotion_scores):

    X_input = pd.DataFrame([emotion_scores])

    # CLAVE
    X_input = X_input.reindex(columns=feature_columns, fill_value=0)

    probs = model_key.predict_proba(X_input)[0]
    top_idx = np.argsort(probs)[-3:][::-1]

    result = []
    for i in top_idx:
        result.append({
            "key": key_map[i],
            "confidence": round(probs[i], 2)
        })

    return result


def analyze_lyrics(text):
    # emociones
    emotions = extract_emotions(text)

    # predicción
    profile = predict_song_profile(emotions)

    # interpretación
    mood = interpret_profile(profile["valence"], profile["energy"])

    # Key
    keys = predict_key(emotions)

    return {
        "emotions": emotions,
        "valence": profile["valence"],
        "energy": profile["energy"],
        "mode": profile["mode"],
        "mood": mood,
        "key_suggestions": keys
    }