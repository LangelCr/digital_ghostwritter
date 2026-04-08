import streamlit as st

from src.model_utils import analyze_lyrics
from src.audio import analyze_audio
from src.llm_utils import generate_music_advice
from src.llm_utils import generate_music_advice_audio
from src.llm_utils import generate_combined_music_advice
from src.chords import generate_chord_audio

import pandas as pd


import plotly.express as px
import plotly.graph_objects as go


st.title("🎧 Digital Ghostwritter")



mode = st.radio("Modo", ["Letra", "Audio", "Ambos"])

text = None
audio = None

if mode in ["Letra", "Ambos"]:
    text = st.text_area("Letra")

if mode in ["Audio", "Ambos"]:
    audio = st.file_uploader("Audio")

if st.button("Analizar"):

    result_text = None
    result_audio = None

    if text:
        result_text = analyze_lyrics(text)
        st.subheader(" 🎤 Resultado letra...")
        #st.json(result_text)

    
    if audio:
        with open("temp.wav", "wb") as f:
            f.write(audio.read())
            result_audio = analyze_audio("temp.wav")
        st.subheader("🎧 Resultado audio...")
        st.json(result_audio)

    # 3️⃣ Combinar resultados y generar recomendación
    if result_text or result_audio:

        # Combinar la info de ambos
        combined_analysis = {
            "mood_text": result_text.get("mood") if result_text else None,
            "valence_text": result_text.get("valence") if result_text else None,
            "energy_text": result_text.get("energy") if result_text else None,
            "mode_text": result_text.get("mode") if result_text else None,
            "keys_text": [k['key'] for k in result_text.get("key_suggestions", [])] if result_text else [],
            "key_audio": result_audio.get("key") if result_audio else None,
            "chords_audio": result_audio.get("chords") if result_audio else [],
            "tempo_audio": result_audio.get("tempo") if result_audio else None,
        }

        # Llamada a tu LLM para análisis + recomendaciones + continuación de letra
        advice = generate_combined_music_advice(result_text, result_audio, text)
        # advice = "💡 Esto es un resultado simulado para pruebas, no se usó OpenAI."
        st.json(result_text)
    

    if result_text:
        
        advice = generate_music_advice(result_text, text)
        
        #advice = "💡 Esto es un resultado simulado para pruebas, no se usó OpenAI."

        scores, translated = result_text["emotions"]
        fig = px.bar(
        x=list(scores.keys()),
        y=list(scores.values()),
        labels={'x':'Emoción', 'y':'Valor'},
        title="🎭 Distribución de emociones de la letra"
        )
        st.plotly_chart(fig)
        
    elif result_audio:

        advice = generate_music_advice_audio(result_audio)

        #advice = "💡 Esto es un resultado simulado para pruebas, no se usó OpenAI."

        chords = result_audio["chords"]
        st.subheader("🎹 Progresión sugerida")
        st.write(" → ".join(chords))
        st.info("Tip: Alternar acordes mayores y menores genera tensión y resolución en la melodía.")


    st.subheader("🎯 Recomendación")
    st.write(advice)


# ================= Sidebar =================
st.sidebar.title("📚 Aprende teoría musical")

st.sidebar.markdown("""
- **Tonalidad:** nota principal de la canción (mayor o menor).
- **Mood:** describe la emoción principal.
- **Chords:** acordes sugeridos.
- **Tempo:** velocidad en BPM.
""")

# Mostrar resultados de texto
if 'result_text' in locals() and result_text:
    st.sidebar.subheader("🎤 Análisis de letra")
    
    # Emociones traducidas al español
    emotion_map = {
        "fear": "Miedo",
        "neutral": "Neutral",
        "anger": "Enojo",
        "sadness": "Tristeza",
        "disgust": "Asco",
        "joy": "Alegría",
        "surprise": "Sorpresa"
    }

    emotions = result_text.get("emotions", {})
    # Convertir probabilidades a % y redondear
    emotions_display = {emotion_map[k]: f"{v*100:.1f}%" for k,v in scores.items()}

    # Mostrar como tabla
    st.sidebar.table(emotions_display.items())

    # Valence y Energy como barras
    valence_pct = int(result_text.get("valence", 0) * 100)
    energy_pct = int(result_text.get("energy", 0) * 100)

    st.sidebar.write("**Valence (Positividad):**")
    st.sidebar.progress(valence_pct)

    st.sidebar.write("**Energía:**")
    st.sidebar.progress(energy_pct)

    # Mood y Mode con emojis
    mood_map = {
        "Intense": "🔥 Intensa",
        "Calm": "😌 Calmante",
        "Happy": "😊 Alegre",
        "Sad": "😢 Triste"
    }
    mode_map = {
        "major": "🎶 Mayor",
        "minor": "🎵 Menor"
    }

    st.sidebar.write(f"**Mood:** {mood_map.get(result_text.get('mood',''), result_text.get('mood',''))}")
    st.sidebar.write(f"**Modo:** {mode_map.get(result_text.get('mode',''), result_text.get('mode',''))}")


    # ----------------- Key suggestions -----------------

    
if 'result_text' in locals() and result_text:  # <-- chequea que exista

    key_suggestions = result_text.get("key_suggestions", [])

    if key_suggestions:
        st.subheader("🎹 Sugerencias de Tonalidad")
        
        # Crear DataFrame
        df_keys = pd.DataFrame(key_suggestions)
        df_keys['confidence'] = df_keys['confidence']*100  # convertir a %
        
        # Mostrar barra
        fig_keys = px.bar(
            df_keys, 
            x='key', 
            y='confidence', 
            text='confidence',
            labels={'key':'Tonalidad', 'confidence':'Confianza (%)'},
            title="💡 Sugerencias de Tonalidad"
        )
        fig_keys.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
        fig_keys.update_layout(yaxis=dict(range=[0,100]))
        st.sidebar.plotly_chart(fig_keys, use_container_width=True)

        # Diccionario educativo de tonalidades
        key_descriptions = {
            "C": "🎵 Alegre, brillante y abierta. Fácil para principiantes.",
            "G": "🎶 Cálida y equilibrada, buena para folk o pop.",
            "D": "🎸 Brillante y energética, ideal para guitarras.",
            "A": "🎹 Optimista y clara, suena bien en acústico.",
            "E": "⚡ Energética y potente, común en rock.",
            "F": "🎼 Suave y melódica, buena para baladas.",
            "B": "🎷 Misteriosa y sofisticada, suena intensa."
        }

        st.markdown("**📝 Qué significa cada Key:**")
        for k in df_keys['key']:
            desc = key_descriptions.get(k, "🎵 Tonalidad general")
            st.markdown(f"- **{k}**: {desc}")
    
    

# Mostrar resultados de audio
if 'result_audio' in locals() and result_audio:
    st.sidebar.subheader("🎧 Análisis de audio")
    st.sidebar.write(f"**Key:** {result_audio.get('key','')}")
    st.sidebar.write(f"**Suggest Chords:** {', '.join(result_audio.get('chords',[]))}")
    st.sidebar.write(f"**Tempo:** {result_audio.get('tempo',0):.1f} BPM")


