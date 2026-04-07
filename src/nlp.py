from transformers import pipeline

emotion_model = None  # inicializamos como None

def get_emotion_model():
    global emotion_model
    if emotion_model is None:
        # Se carga solo la primera vez
        emotion_model = pipeline(
            "text-classification",
            model="mrm8488/distilbert-base-multilingual-cased-finetuned-emotion",
            top_k=None
        )
    return emotion_model

def extract_emotions(text):
    model = get_emotion_model()

    result = model(
        text,
        truncation=True,
        max_length=300
    )[0]

    scores = {item["label"].lower(): item["score"] for item in result}
    all_emotions = ["surprise", "neutral", "disgust", "anger", "joy", "fear", "sadness"]
    for e in all_emotions:
        scores.setdefault(e, 0)

    return scores