import random
import sounddevice as sd
import numpy as np
import json
import os
import sys
import re

# Sampling rate for sound generation (in Hz)
sampling_rate = 44100

# Constants for tempered scale calculations
scale = 440
ratio = 2 ** (1 / 12)

# Create a dictionary of notes with offsets from 'A', including enharmonic equivalents
notes = {'A1': -24,
         'A#1': -23, 'Bb1': -23,
         'B1': -22,
         'C1': -21,
         'C#1': -20, 'Db1': -20,
         'D1': -19,
         'D#1': -18, 'Eb1': -18,
         'E1': -17,
         'F1': -16,
         'F#1': -15, 'Gb1': -15,
         'G1': -14,
         'G#1': -13, 'Ab1': -13,
         'A2': -12,
         'A#2': -11, 'Bb2': -11,
         'B2': -10,
         'C2': -9,
         'C#2': -8, 'Db2': -8,
         'D2': -7,
         'D#2': -6, 'Eb2': -6,
         'E2': -5,
         'F2': -4,
         'F#2': -3, 'Gb2': -3,
         'G2': -2,
         'G#2': -1, 'Ab2': -1,
         'A3': 0,
         'A#3': 1, 'Bb3': 1,
         'B3': 2,
         'C3': 3,
         'C#3': 4, 'Db3': 4,
         'D3': 5,
         'D#3': 6, 'Eb3': 6,
         'E3': 7,
         'F3': 8,
         'F#3': 9, 'Gb3': 9,
         'G3': 10,
         'G#3': 11, 'Ab3': 11,
         'A4': 12,
         'A#4': 13, 'Bb4': 13,
         'B4': 14,
         'C4': 15,
         'C#4': 16, 'Db4': 16,
         'D4': 17,
         'D#4': 18, 'Eb4': 18,
         'E4': 19,
         'F4': 20,
         'F#4': 21, 'Gb4': 21,
         'G4': 22,
         'G#4': 23, 'Ab4': 23,
         'A5': 24,
         'A#5': 25, 'Bb5': 25,
         'B5': 26,
         'C5': 27,
         'C#5': 28, 'Db5': 28,
         'D5': 29,
         'D#5': 30, 'Eb5': 30,
         'E5': 31,
         'F5': 32,
         'F#5': 33, 'Gb5': 33,
         'G5': 34,
         'G#5': 35, 'Ab5': 35,
         'A6': 36,}

# Create a dictionary of frequencies for each note
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

# Use fade to avoid clipping between notes.
def apply_fade(waveform, fade_samples):
    fade_in = np.linspace(0, 1, fade_samples)
    fade_out = np.linspace(1, 0, fade_samples)
    waveform[:fade_samples] *= fade_in
    waveform[-fade_samples:] *= fade_out
    return waveform

# Function to play a song specified by song_name, plays audio
def play_song(song_name):
    song_data = load_song_from_json(song_name)
    if not song_data:
        print(f"Error: Song '{song_name}' not found.")
        return
    
    # Initialize an empty array for the final waveform
    final_waveform = np.array([])

    # Get the BPM and default duration
    bpm = song_data['bpm']
    default_duration = 60 / bpm 

    # Define the number of samples to use for the fade effect
    fade_samples = int(0.006 * sampling_rate)  # 1% of the sampling rate

    for note, custom_duration in song_data['notes']:
        freq = tempered_notes.get(note)

        # Reset to default duration at the beginning of each iteration
        duration = int(sampling_rate * default_duration)
        
        # Apply a custom duration if specified
        if custom_duration:
            if isinstance(custom_duration, str):
                custom_duration = eval(custom_duration)  # Evaluate the string to get the numeric value
            duration = int(sampling_rate * (default_duration * custom_duration))

        time_values = np.linspace(0, duration / sampling_rate, duration, endpoint=False)
        waveform = 0.5 * np.sin(2 * np.pi * freq * time_values)

        # Apply fade
        waveform = apply_fade(waveform, fade_samples)

        # Append to the final waveform
        final_waveform = np.concatenate((final_waveform, waveform))

    # Apply fade-out to the final waveform
    final_waveform = apply_fade(final_waveform, fade_samples)

    # Play the final waveform
    sd.play(final_waveform, samplerate=sampling_rate)
    sd.wait()

# Function to play a random song from available JSON files in 'songs' directory
def play_random_song():
    song_files = [f for f in os.listdir('songs') if os.path.isfile(os.path.join('songs', f)) and f.endswith('.json')]
    if not song_files:
        print("Error: No songs found.")
        return

    song_file = random.choice(song_files)
    song_name = os.path.splitext(song_file)[0]
    play_song(song_name)

# Function to add a new song or modify an existing one in 'songs' directory
def add_song():
    while True:
        song_name = input("Enter the name of the song: ")
        if re.match("^[a-zA-Z0-9_\-]+$", song_name):
            break
        else:
            print(f"Error: '{song_name}' contains invalid characters. Please use only letters, numbers, underscores, and hyphens.")
    
    # Check if the song already exists
    file_path = f'songs/{song_name}.json'
    if os.path.exists(file_path):
        print("This song already exists.")
        action = input("Would you like to append new notes or redo the last entry? Type 'append' or 'back': ")
        if action.lower() == 'append':
            with open(file_path, 'r', encoding='utf-8') as file:
                existing_song_data = json.load(file)
                notes = existing_song_data.get('notes', [])
                bpm = existing_song_data.get('bpm', 120)
        elif action.lower() == 'back':
            with open(file_path, 'r', encoding='utf-8') as file:
                existing_song_data = json.load(file)
                notes = existing_song_data.get('notes', [])
                if len(notes) > 0:
                    notes.pop()
                bpm = existing_song_data.get('bpm', 120)
        else:
            print("Invalid action. Exiting.")
            return
    else: # Song does not exist yet
        notes = []
        while True:
            bpm_input = input("Enter the BPM (Beats Per Minute): ")
            if not bpm_input:
                bpm = 120
                break
            try:
                bpm = int(bpm_input)
                if bpm <= 0:
                    print("Error: BPM must be a positive integer.")
                else:
                    break
            except ValueError:
                print("Error: BPM must be a positive integer.")

    # Collect notes and custom durations
    while True:
        entry = input("Enter a note and optional custom duration (e.g., 'C#4' or 'A5 1/3'), or 'stop' to finish, or 'back' to redo the last entry: ")

        if entry.lower() == 'stop':
            break

        if entry.lower() == 'back':
            if len(notes) > 0:
                notes.pop()
                print("Last entry removed.")
            else:
                print("Error: No previous entry to remove.")
            continue

        parts = entry.split()
        note = parts[0][0].upper() + parts[0][1:]
        
        if len(parts) > 1:
            custom_duration = parts[1]
        else:
            custom_duration = None

        if note not in tempered_notes:
            print(f"Error: '{note}' is not a valid note. Please enter a valid note.")
            continue

        notes.append([note, custom_duration])

    # Create JSON object
    song_data = {
        "notes": notes,
        "bpm": bpm
    }

    # Write to file
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(song_data, file, ensure_ascii=False, indent=4)

    play_song(song_name)


# Main script logic for executing functions based on command-line arguments
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
