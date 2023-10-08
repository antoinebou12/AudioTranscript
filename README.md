# Speech Recognition CLI

## Description

This project is a Command Line Interface (CLI) application that transcribes audio files using the Google Speech Recognition API. It leverages the `pydub` library to split audio into smaller chunks and uses the `speech_recognition` library to transcribe these chunks.

## Features

- Transcribes audio files into text
- Splits audio into smaller chunks based on silence for efficient transcription
- Allows customization of various parameters like silence length, silence threshold, and language
- Rich console output for user-friendly interaction

## Requirements

- Python 3.x
- pydub
- speech_recognition
- rich
- typer
- dotenv

## Installation

1. Clone the repository
   ```
   git clone https://github.com/yourusername/speech-recognition-cli.git
   ```

2. Navigate to the project directory
   ```
   cd speech-recognition-cli
   ```

3. Install the required packages
   ```
   pip install -r requirements.txt
   ```

4. Create a `.env` file and add your AWS credentials
   ```
   AWS_ACCESS_KEY_ID=your_access_key
   AWS_SECRET_ACCESS_KEY=your_secret_key
   AWS_BUCKET_NAME=your_bucket_name
   ```

## Usage

To run the CLI application, navigate to the project directory and run the following command:

```
python main.py --path <audio_file_path> --min-silence-len <min_silence_length> --silence-thresh <silence_threshold> --keep-silence <keep_silence_duration> --language <language_code>
```

### Parameters:

- `--path`: Path of the audio file to transcribe.
- `--min-silence-len`: Minimum length of silence required to detect the end of a speech segment in milliseconds.
- `--silence-thresh`: Threshold value in dBFS below which the audio is considered silent.
- `--keep-silence`: Duration of silence to be kept at the beginning and end of each chunk in milliseconds.
- `--language`: Language code of the audio file to be transcribed.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

[MIT License](LICENSE)
