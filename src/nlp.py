from transformers import pipeline
from deep_translator import GoogleTranslator



emotion_model = pipeline(
    "text-classification",
    model="j-hartmann/emotion-english-distilroberta-base",
    top_k=None
)

def extract_emotions(text):

    translated = GoogleTranslator(source='auto', target='en').translate(text)

    result = emotion_model(
        translated,
        truncation=True,
        max_length=300
    )[0]

    scores = {item["label"]: item["score"] for item in result}

    all_emotions = ["surprise", "neutral", "disgust", "anger", "joy", "fear", "sadness"]

    for e in all_emotions:
        scores.setdefault(e, 0)

    return scores, translated

