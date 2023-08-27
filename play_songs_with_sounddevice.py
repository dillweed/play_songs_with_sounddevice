import random
import sounddevice as sd
import numpy as np
import json
import os
import sys

# Constants for sound generation
sampling_rate = 44100

# Constants and tempered_notes setup
scale = 440
ratio = 2 ** (1 / 12)

# Define the note offsets from 'A'
notes = {'A1': -24,
         'A#1': -23,
         'B1': -22,
         'C1': -21,
         'C#1': -20,
         'D1': -19,
         'D#1': -18,
         'E1': -17,
         'F1': -16,
         'F#1': -15,
         'G1': -14,
         'G#1': -13,
         'A2': -12,
         'A#2': -11,
         'B2': -10,
         'C2': -9,
         'C#2': -8,
         'D2': -7,
         'D#2': -6,
         'E2': -5,
         'F2': -4,
         'F#2': -3,
         'G2': -2,
         'G#2': -1,
         'A3': 0,
         'A#3': 1,
         'B3': 2,
         'C3': 3,
         'C#3': 4,
         'D3': 5,
         'D#3': 6,
         'E3': 7,
         'F3': 8,
         'F#3': 9,
         'G3': 10,
         'G#3': 11,
         'A4': 12,
         'A#4': 13,
         'B4': 14,
         'C4': 15,
         'C#4': 16,
         'D4': 17,
         'D#4': 18,
         'E4': 19,
         'F4': 20,
         'F#4': 21,
         'G4': 22,
         'G#4': 23,
         'A5': 24,
         'A#5': 25,
         'B5': 26,
         'C5': 27,
         'C#5': 28,
         'D5': 29,
         'D#5': 30,
         'E5': 31,
         'F5': 32,
         'F#5': 33,
         'G5': 34,
         'G#5': 35,
         'A6': 36,}

# Create a dictionary of tempered notes
tempered_notes = {}
for note in notes:
    freq = scale * ratio ** notes[note]
    tempered_notes[note] = freq

# Function to load song data from a JSON file
def load_song_from_json(song_name):
    file_path = f'songs/{song_name}.json'
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    return None

# Function to play a song
def play_song(song_name):
    song_data = load_song_from_json(song_name)
    if not song_data:
        print(f"Error: Song '{song_name}' not found.")
        return
    
    # Initialize an empty array for the final waveform
    final_waveform = np.array([])

    default_duration = song_data['default_duration']
    duration = int(sampling_rate * (default_duration / 1000))

    # Apply fade-in and fade-out
    fade_samples = int(0.01 * sampling_rate)
    fade_in = np.linspace(0, 1, fade_samples)
    fade_out = np.linspace(1, 0, fade_samples)

    for note, custom_duration in song_data['notes']:
        freq = tempered_notes.get(note)

        # Reset to default duration at the beginning of each iteration
        duration = int(sampling_rate * (default_duration / 1000))
        
        # Apply a custom duration if specified
        if custom_duration:
            if isinstance(custom_duration, str):
                custom_duration = eval(custom_duration)  # Evaluate the string to get the numeric value
            duration = int(sampling_rate * (default_duration * custom_duration / 1000))

        time_values = np.linspace(0, duration / sampling_rate, duration, endpoint=False)
        waveform = 0.5 * np.sin(2 * np.pi * freq * time_values)

        # Apply fade-in and fade-out
        waveform[:fade_samples] *= fade_in
        waveform[-fade_samples:] *= fade_out

        # Append to the final waveform
        final_waveform = np.concatenate((final_waveform, waveform))

    # Apply fade-out to the final waveform
    fade_out = np.linspace(1, 0, fade_samples)
    final_waveform[-fade_samples:] *= fade_out

    # Play the final waveform
    sd.play(final_waveform, samplerate=sampling_rate)
    sd.wait()

# Define a function to play a random song
def play_random_song():
    song_files = [f for f in os.listdir('songs') if os.path.isfile(os.path.join('songs', f)) and f.endswith('.json')]
    if not song_files:
        print("Error: No songs found.")
        return

    song_file = random.choice(song_files)
    song_name = os.path.splitext(song_file)[0]
    play_song(song_name)

def add_song():
    # Ask for song name
    song_name = input("Enter the name of the song: ")

    # Ask for default duration
    default_duration = int(input("Enter the default note duration in milliseconds: "))

    # Initialize notes array
    notes = []

    # Collect notes and custom durations
    while True:
        entry = input("Enter a note and optional custom duration (e.g., 'C#4 1/3'), or 'stop' to finish: ")
        
        if entry.lower() == 'stop':
            break

        parts = entry.split()
        note = parts[0]
        
        if len(parts) > 1:
            custom_duration = parts[1]
        else:
            custom_duration = None

        notes.append([note, custom_duration])

    # Create JSON object
    song_data = {
        "notes": notes,
        "default_duration": default_duration
    }

    # Write to file
    file_path = f"songs/{song_name}.json"
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(song_data, file, ensure_ascii=False, indent=4)

    play_song(song_name)

# If this script is being run directly (rather than imported)
if __name__ == "__main__":
    if len(sys.argv) > 1:
        # If an argument is given
        arg = sys.argv[1].lower()
        if arg == 'add':
            # If the argument is 'add', call the add_song function
            add_song()
        else:
            # Otherwise, play the song named in the argument
            play_song(arg)
    else:
        # If no argument is given, play a random song
        play_random_song()
