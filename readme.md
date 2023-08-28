# Python Melody Player with SoundDevice

A Python script to record and play synthezied monophonic songs using the SoundDevice library. It's a fun way to add audible alerts to a script. (Like a washing machine jingle)

## Features

- Play individual notes with custom duration.
- Play songs from JSON files.
- Play random songs from a list.
- Add new songs via user input.

## Requirements

- Python 3.x
- NumPy
- SoundDevice

You can install the required packages using pip:

```
pip install numpy sounddevice
```

## How to Use

### Playing a Random Song

Execute the script:

```
python play_songs_with_sounddevice.py
```

### Playing a Specific Song

To play a specific song stored as a JSON file under the songs directory:

```
python play_songs_with_sounddevice.py sweet_child
```

### Adding a New Song

To add a new song:

```
python play_songs_with_sounddevice.py add
```

Follow the prompts to enter the song name, beats per minute, and individual notes with optional custom durations.

## JSON Song File Structure

Songs are stored as JSON files. The `notes` array contains sequential notes from A1 through A6 with the following structure:

- `note`: The note name (e.g. `A1`, `D#4`, `Eb5`, `C#2`). Note that an 'Ab' (A-flat) is noted with the octave preceding the A immediately above. For example, `Ab5` is just before `A6`.
- `duration`: The multiplier of the beat length expressed either as a fraction or decimal. A null value will use the default duration calculated from the BPM. 

```json
{
    "notes": [
        ["A1", null],
        ["D#4", 2],
        ["Eb5", "1/3"],
        ["A6", 0.25]
    ],
    "bpm": 120
}
```

## Project Structure

- `songs/`: Directory containing song JSON files
- `play_songs_with_sounddevice.py`: Main Python script

## Contributing

Feel free to fork the repository and submit pull requests.

## Troubleshooting

> Add common issues and their solutions here.

- TODO: Remap scale to match [standard octave numbering](https://www.vibrationdata.com/tutorials2/piano.pdf). 
- TODO: Transcribe the Frigidaire jingles. 

## License

This project is licensed under the MIT License.
