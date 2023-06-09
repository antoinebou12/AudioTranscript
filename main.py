import os
from typing import Optional
import typer
from pydub import AudioSegment
from pydub.silence import split_on_silence
import speech_recognition as sr
from rich.console import Console
from rich.progress import track

from dotenv import load_dotenv
load_dotenv(".env")


console = Console()

app = typer.Typer()


def transcribe_audio_file(
    path: str,
    min_silence_len: int = 500,
    silence_thresh: int = -30,
    keep_silence: int = 500,
    language: Optional[str] = None,
):  # sourcery skip: raise-specific-error
    """
    Transcribes an audio file using Google Speech Recognition API.

    Args:
        path (str): Path of the audio file.
        min_silence_len (int, optional): Minimum length of silence required to detect the end of a speech segment in milliseconds. Defaults to 500.
        silence_thresh (int, optional): Threshold value in dBFS below which the audio is considered silent. Defaults to -30.
        keep_silence (int, optional): Duration of silence to be kept at the beginning and end of each chunk in milliseconds. Defaults to 500.
        language (str, optional): Language code of the audio file to be transcribed. If None, auto-detects the language. Defaults to None.

    Returns:
        str: Transcription of the audio file.
    """
    console.print(f"Transcribing audio file: {path}")
    # create a speech recognition object
    console.print("Creating speech recognition object...")
    r = sr.Recognizer()
    # open the audio file using pydub
    console.print("Opening audio file...")
    sound = AudioSegment.from_wav(path)
    # split audio sound where silence is `min_silence_len` or more and get chunks
    console.print("Splitting audio file into chunks...")
    chunks = split_on_silence(sound, min_silence_len=min_silence_len,
                              silence_thresh=sound.dBFS + silence_thresh, keep_silence=keep_silence)

    # create a directory to store the audio chunks
    folder_name = "audio-chunks"
    if not os.path.isdir(folder_name):
        os.mkdir(folder_name)

    console.print(f"Splitting audio file into {len(chunks)} chunks")

    with console.status("[bold green]Transcribing...") as status:
        whole_text = ""
        for i, audio_chunk in track(enumerate(chunks, start=1), total=len(chunks)):
            chunk_filename = os.path.join(folder_name, f"chunk{i}.wav")
            audio_chunk.export(chunk_filename, format="wav")

            console.print(f"Processing chunk {i} of {len(chunks)}")

            with sr.AudioFile(chunk_filename) as source:
                audio_listened = r.record(source)
                try:
                    console.print("Recognizing...")
                    if not os.getenv("AWS_ACCESS_KEY_ID") or not os.getenv("AWS_SECRET_ACCESS_KEY") or not os.getenv("AWS_BUCKET_NAME"):
                        raise Exception("AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY and AWS_BUCKET_NAME must be set in .env file")
                    text = r.recognize_amazon(audio_listened,
                                              region="us-east-1",
                                              access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
                                              secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
                                              bucket_name=os.getenv("AWS_BUCKET_NAME"),
                                              job_name="speech-recognition-cli2-job",
                                              file_key="speech-recognition-cli",
                                              )
                except sr.UnknownValueError:
                    text = ""

                whole_text += f"{text} "

    # print the complete text transcription
    console.print("\n[bold green]Complete Text Transcription:[/bold green]")
    console.print(whole_text)

    return whole_text


@app.command()
def main(
    path: str = typer.Argument(
        "caro.wav", help="Path of the audio file to transcribe."),
    min_silence_len: int = typer.Option(
        500,
        "--min-silence-len",
        "-m",
        help="Minimum length of silence required to detect the end of a speech segment in milliseconds.",
    ),
    silence_thresh: int = typer.Option(
        -14,
        "--silence-thresh",
        "-s",
        help="Threshold value in dBFS below which the audio is considered silent.",
    ),
    keep_silence: int = typer.Option(
        500,
        "--keep-silence",
        "-k",
        help="Duration of silence to be kept at the beginning and end of each chunk in milliseconds.",
    ),
    language: Optional[str] = typer.Option(
        "es-co",
        "--language",
        "-l",
        help="Language code of the audio file to be transcribed. If None, auto-detects the language.",
    ),
):
    """
    Transcribes an audio file using Google Speech Recognition API.
    """
    console.print(
        "[bold green]Welcome to Speech Recognition CLI![/bold green]")

    transcribe_audio_file(
        path=path,
        min_silence_len=min_silence_len,
        silence_thresh=silence_thresh,
        keep_silence=keep_silence,
        language=language,
    )

    console.print(
        "[bold green]Thank you for using Speech Recognition CLI![/bold green]")

    return 0


if __name__ == "__main__":
    typer.run(main)
