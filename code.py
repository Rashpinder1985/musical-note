import streamlit as st
import numpy as np
import sounddevice as sd
import time
from scipy.signal import square, sawtooth

# Constants
SAMPLE_RATE = 44100  # 44.1 kHz sample rate
DURATION = 0.5  # Default duration per note (seconds)

# Note Frequencies (in Hz)
NOTE_FREQUENCIES = {
    "C4": 261.63, "D4": 293.66, "E4": 329.63, "F4": 349.23, "G4": 392.00, "A4": 440.00, "B4": 493.88,
    "C5": 523.25, "D5": 587.33, "E5": 659.25, "F5": 698.46, "G5": 783.99, "A5": 880.00, "B5": 987.77
}


# Generate waveform
def generate_waveform(wave_type, frequency, duration):
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration), endpoint=False)
    if wave_type == "Sine":
        wave = np.sin(2 * np.pi * frequency * t)
    elif wave_type == "Square":
        wave = square(2 * np.pi * frequency * t)
    elif wave_type == "Sawtooth":
        wave = sawtooth(2 * np.pi * frequency * t)
    else:
        wave = np.zeros_like(t)
    return wave


# Play melody
def play_melody(notes, wave_type, duration, tempo):
    silence = np.zeros(int(SAMPLE_RATE * 0.05))  # Short silence between notes
    full_wave = np.array([])

    for note in notes.split():
        freq = NOTE_FREQUENCIES.get(note, 0)  # Default to silence if note not found
        if freq > 0:
            wave = generate_waveform(wave_type, freq, duration)
            full_wave = np.concatenate((full_wave, wave, silence))

    sd.play(full_wave, SAMPLE_RATE)
    time.sleep(len(full_wave) / SAMPLE_RATE)
    sd.stop()


# Streamlit UI
st.title("Music Notation Synthesizer")

# Select waveform
type_of_wave = st.selectbox("Select Waveform", ["Sine", "Square", "Sawtooth"])

# Input melody (space-separated notes)
melody_input = st.text_input("Enter melody (e.g., C4 D4 E4 F4 G4)", "C4 D4 E4")

# Select note duration
note_duration = st.slider("Note Duration (seconds)", 0.1, 1.0, 0.5)

# Select tempo (affects silence between notes)
tempo = st.slider("Tempo (BPM)", 60, 200, 120)

# Play button
if st.button("Play Melody"):
    play_melody(melody_input, type_of_wave, note_duration, tempo)
