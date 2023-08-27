# Python MIDI Player with SoundDevice

A Python script to play musical notes and simple songs using the SoundDevice library.

## Features

- Play individual notes with specified or default durations.
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

Follow the prompts to enter the song name, default note duration, and individual notes with optional custom durations.

## JSON Song File Structure

Songs are stored as JSON files with the following structure:

```json
{
    "notes": [
        ["C3", "1/4"],
        ["D3", "1/4"],
        ["F3", "1/4"],
        ["D3", "1/4"]
    ],
    "default_duration": 500
}
```

## Project Structure

- `songs/`: Directory containing song JSON files
- `play_songs_with_sounddevice.py`: Main Python script

## Contributing

Feel free to fork the repository and submit pull requests.

## Troubleshooting

> Add common issues and their solutions here.

## License

This project is licensed under the MIT License.
