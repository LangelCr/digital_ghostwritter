import librosa
import numpy as np

NOTE_MAP = ['C', 'C#', 'D', 'D#', 'E', 'F',
            'F#', 'G', 'G#', 'A', 'A#', 'B']

def load_audio(file_path):
    """
    Carga un archivo de audio y devuelve la señal y la frecuencia de muestreo.
    
    Args:
        file_path (str): La ruta al archivo de audio.

    Returns:
        y (np.ndarray): La señal de audio.
        sr (int): La frecuencia de muestreo.
    """ 
    
    
    y, sr = librosa.load(file_path, sr=None)
    return y, sr

def extract_features(y, sr):
    """
    Extrae features clave del audio.
    
    Returns:
        tempo (float)
        chroma_mean (array)
    """
    # 🎵 tempo
    tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
    
    # 🎹 chroma
    chroma = librosa.feature.chroma_stft(y=y, sr=sr)
    chroma_mean = chroma.mean(axis=1)
    
    return tempo, chroma_mean
    

def detect_key(chroma_mean):
    """
    Detecta la nota dominante.
    
    Returns:
        key (str)
    """
    note_index = np.argmax(chroma_mean)
    key = NOTE_MAP[note_index]
    return key

def detect_mode(tempo, chroma_mean):
    """
    Detecta modo basado en heurísticas simples.
    
    Returns:
        "major" o "minor"
    """
    energy = np.mean(chroma_mean)
    
    if tempo < 90 and energy < 0.5:
        return "minor"
    else:
        return "major"
    
def get_chords(key, mode):
    """
    Genera progresión de acordes básica.
    """
    if mode == "minor":
        return [f"{key}m", "F", "C", "G"]
    else:
        return [key, "G", "Am", "F"]
    

def analyze_audio(file_path):
    """
    Pipeline completo de análisis de audio.
    
    Returns:
        dict con resultados
    """
    y, sr = load_audio(file_path)
    
    tempo, chroma_mean = extract_features(y, sr)
    
    key = detect_key(chroma_mean)
    
    mode = detect_mode(tempo, chroma_mean)
    
    chords = get_chords(key, mode)
    
    return {
        "tempo": float(tempo[0]),
        "key": key,
        "mode": mode,
        "chords": chords
    }