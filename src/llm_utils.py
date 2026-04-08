# src/llm_utils.py
from openai import OpenAI
import os
from dotenv import load_dotenv

# cargar variables de entorno
load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))



def generate_music_advice(analysis, user_text):
    """
    Usa ChatGPT para dar recomendaciones musicales
    basadas en el output de tu modelo
    """

    prompt = f"""
    Eres un productor musical profesional.

    IMPORTANTE:
    - NO hagas preguntas
    - NO invites al usuario a continuar la conversación
    - NO uses frases como "¿quieres que...?"
    - NO agregues cierres conversacionales
    - SOLO entrega un análisis completo en un solo bloque

    Un usuario escribió esta letra:
    "{user_text}"

    El análisis del modelo es:
    - Mood: {analysis['mood']}
    - Valence: {analysis['valence']}
    - Energy: {analysis['energy']}
    - Mode: {analysis['mode']}
    - Keys sugeridas: {[k['key'] for k in analysis['key_suggestions']]}

    Tu tarea:
    1. Continuar la letra generando entre 4 y 8 nuevas líneas, respetando rimas, ritmo y estilo de la letra original
    2. Explicar el mood y el sentimiento principal de la canción
    3. Recomendar estilo musical y progresiones sugeridas
    4. Dar consejos prácticos (tempo, instrumentos, dinámica, ambiente)
    5. Entregar todo en un solo bloque, claramente separado: primero la continuación de la letra, luego el análisis y consejos

    Responde únicamente con contenido útil, sin saludos ni cierres.

    Responde en español, tono profesional pero cercano.
    """

    response = client.chat.completions.create(
        model="gpt-4.1-mini",  # rápido y barato
        messages=[
            {"role": "system", "content": "Eres un experto letrista y productor musical."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7
    )

    return response.choices[0].message.content

def generate_music_advice_audio(audio_analysis):
    """
    Usa ChatGPT para dar recomendaciones técnicas de producción
    basadas en el análisis de audio.
    """
    prompt = f"""
    Eres un productor musical profesional.
    ANALIZA el siguiente audio y da recomendaciones técnicas.

    Análisis de audio:
    - Tempo: {audio_analysis.get("tempo")}
    - Key: {audio_analysis.get("key")}
    - Mode: {audio_analysis.get("mode")}
    - Chords: {audio_analysis.get("chords")}

    Tu tarea:
    1. Explicar el vibe del audio
    2. Recomendar progresión, instrumentos, estilo
    3. Dar consejos prácticos de producción (tempo, energía, efectos)

    Termina la respuesta en un solo bloque, sin preguntas ni interacción.
    """

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": "Eres un experto en producción musical."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7
    )

    return response.choices[0].message.content


def generate_combined_music_advice(result_text, result_audio, user_text):
    """
    Genera un análisis musical y recomendaciones combinadas
    tomando en cuenta la letra y el audio.
    """

    # Extraer datos de letra
    mood = result_text.get("mood") if result_text else None
    valence = result_text.get("valence") if result_text else None
    energy = result_text.get("energy") if result_text else None
    mode = result_text.get("mode") if result_text else None
    keys_text = [k["key"] for k in result_text.get("key_suggestions", [])] if result_text else []

    # Extraer datos de audio
    key_audio = result_audio.get("key") if result_audio else None
    chords_audio = result_audio.get("chords") if result_audio else []
    tempo_audio = result_audio.get("tempo") if result_audio else None

    # Preparar prompt para el LLM
    prompt = f"""
    Eres un productor musical profesional.

    USO:
    - Analiza letra y audio de la canción.
    - Entrega recomendaciones completas, sin preguntas ni cierres conversacionales.
    - Incluye análisis lírico, continuación de letra con rimas, estilo sugerido, progresiones, key y consejos prácticos.

    Datos disponibles:

    Letra del usuario:
    \"\"\"{user_text}\"\"\"

    Análisis de letra:
    - Mood: {mood}
    - Valence: {valence}
    - Energy: {energy}
    - Mode: {mode}
    - Keys sugeridas: {keys_text}#

    Análisis de audio:
    - Key detectada: {key_audio}
    - Acordes: {chords_audio}
    - Tempo: {tempo_audio}

    Instrucciones:
    1. Explica brevemente el mood y la energía de la canción.
    2. Recomienda un estilo o género musical acorde.
    3. Sugiere progresiones de acordes o "vibe" basadas en key detectada.
    4. Propón continuación de letra con rimas coherentes.
    5. Da consejos prácticos: tempo, instrumentos, dinámica, armonización.

    Responde en español, tono profesional pero cercano, en un solo bloque.
    """

    # Llamada al LLM (simulación si quieres probar offline)
    ## Descomenta la sección de OpenAI o HF si quieres usar el modelo real
    #"""
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": "Eres un experto en producción musical."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7
    )
    return response.choices[0].message.content
    #"""
    #"""

    # Para pruebas offline / sin consumir créditos
    #simulated_response = f"""
    #🎵 Análisis lírico:
    #Mood: {mood} - Valence: {valence}, Energy: {energy}
    #Modo: {mode}, Keys: {', '.join(keys_text)}

    #🎸 Estilo sugerido: Pop/Rock moderno, con instrumentación ligera y sintetizadores.

    #🎹 Progresión recomendada: {' → '.join(chords_audio) if chords_audio else 'C - G - Am - F'}

    #✍️ Continuación de letra (rimas sugeridas):
    #"Y en el viento escucho tu voz,
    #caminando juntos hacia la luz."

    #💡 Consejos prácticos:
    #- Tempo: {tempo_audio} BPM (aprox.)
    #- Instrumentos sugeridos: guitarra, bajo, batería, sintetizador
    #- Alterna acordes mayores y menores para generar tensión y resolución.
    #- Mantén dinámica progresiva según mood y energía detectada.
    #"""
    #return simulated_response