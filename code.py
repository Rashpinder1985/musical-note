import streamlit as st
import numpy as np
from pydub import AudioSegment
from pydub.generators import Sine, Square, Sawtooth
import simpleaudio as sa
import time

# Constants
SAMPLE_RATE = 44100  # 44.1 kHz sample rate
DURATION = 0.5  # Default duration per note (seconds)

# Note Frequencies (in Hz)
NOTE_FREQUENCIES = {
    "C4": 261.63, "D4": 293.66, "E4": 329.63, "F4": 349.23, "G4": 392.00, "A4": 440.00, "B4": 493.88,
    "C5": 523.25, "D5": 587.33, "E5": 659.25, "F5": 698.46, "G5": 783.99, "A5": 880.00, "B5": 987.77
}


# Generate waveform using pydub generators
def generate_waveform(wave_type, frequency, duration):
    if wave_type == "Sine":
        wave = Sine(frequency).to_audio_segment(duration * 1000)  # duration in milliseconds
    elif wave_type == "Square":
        wave = Square(frequency).to_audio_segment(duration * 1000)
    elif wave_type == "Sawtooth":
        wave = Sawtooth(frequency).to_audio_segment(duration * 1000)
    else:
        wave = AudioSegment.silent(duration * 1000)  # Generate silence if invalid type
    return wave


# Play melody using pydub
def play_melody(notes, wave_type, duration, tempo):
    silence_duration = 50  # 50ms silence between notes
    full_wave = AudioSegment.silent(0)  # Start with no sound

    for note in notes.split():
        freq = NOTE_FREQUENCIES.get(note, 0)  # Default to silence if note not found
        if freq > 0:
            wave = generate_waveform(wave_type, freq, duration)
            full_wave += wave
            # Add a short silence between notes
            full_wave += AudioSegment.silent(silence_duration)

    # Play the full melody using simpleaudio
    play_obj = sa.play_buffer(full_wave.raw_data, num_channels=full_wave.channels,
                              bytes_per_sample=full_wave.sample_width, sample_rate=full_wave.frame_rate)
    play_obj.wait_done()


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
