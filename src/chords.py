import numpy as np
import soundfile as sf

# frecuencias base
NOTE_FREQ = {
    "C": 261.63,
    "D": 293.66,
    "E": 329.63,
    "F": 349.23,
    "G": 392.00,
    "A": 440.00,
    "B": 493.88
}

def get_chord_notes(chord):
    root = chord[0]

    freq = NOTE_FREQ.get(root, 261.63)

    if "m" in chord:  # menor
        return [freq, freq*1.2, freq*1.5]
    else:  # mayor
        return [freq, freq*1.25, freq*1.5]


def generate_chord_audio(chord, duration=2, sr=44100):
    t = np.linspace(0, duration, int(sr * duration))

    notes = get_chord_notes(chord)

    signal = sum(np.sin(2 * np.pi * f * t) for f in notes)

    signal /= np.max(np.abs(signal))

    filename = f"{chord}.wav"
    sf.write(filename, signal, sr)

    return filename