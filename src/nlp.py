from transformers import pipeline
import os

emotion_model = pipeline(
    "text-classification",
    model="mrm8488/distilbert-base-multilingual-cased-finetuned-emotion",
    top_k=None,
    use_auth_token=os.environ.get("HUGGINGFACE_TOKEN")
)

def extract_emotions(text):
    result = emotion_model(
        text,
        truncation=True,
        max_length=300
    )[0]

    scores = {item["label"]: item["score"] for item in result}

    all_emotions = ["surprise", "neutral", "disgust", "anger", "joy", "fear", "sadness"]

    for e in all_emotions:
        scores.setdefault(e, 0)

    return scores