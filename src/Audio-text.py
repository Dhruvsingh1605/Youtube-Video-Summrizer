import os
import sys
import logging
from groq import Groq
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
api_key = os.getenv("GROQ_API_KEY")

# Ensure required directories exist
for d in ('Data', 'text-data', 'logs'):
    os.makedirs(d, exist_ok=True)

# Configure logging
logging.basicConfig(
    filename=os.path.join('logs', 'Audio-to-Text.log'),
    filemode='a',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logging.info("Starting transcription pipeline (no chunking)")


def transcribe_and_save(audio_path: str) -> str:
    """
    Transcribes the given audio file via Groq ASR
    and saves the text output into 'text-data/'.
    Logs each step into 'logs/Audio-to-Text.log'.
    """
    if not api_key:
        logging.error("GROQ_API_KEY not found in environment.")
        raise RuntimeError("GROQ_API_KEY must be set in environment variables.")

    client = Groq(api_key=api_key)
    logging.info(f"Transcribing audio: {audio_path}")
    
    try:
        with open(audio_path, 'rb') as audio_file:
            transcription = client.audio.transcriptions.create(
                model='whisper-large-v3-turbo',
                file=audio_file,
                response_format='json'
            )
        # Extract text from Transcription object
        transcript_text = transcription.text

        # Save transcript to text-data folder
        base_name = os.path.splitext(os.path.basename(audio_path))[0]
        text_path = os.path.join('text-data', f"{base_name}.txt")
        with open(text_path, 'w', encoding='utf-8') as txt_f:
            txt_f.write(transcript_text)

        logging.info(f"Transcription successful. Saved to: {text_path}")
        return text_path

    except Exception as e:
        logging.error(f"Error transcribing audio {audio_path}: {e}")
        raise


if __name__ == "__main__":
    # Locate the first WAV file in Data/
    wav_files = [f for f in os.listdir('Data') if f.lower().endswith('.wav')]
    if not wav_files:
        logging.error("No WAV file found in Data/")
        sys.exit(1)
    audio_file = os.path.join('Data', wav_files[0])

    try:
        result_path = transcribe_and_save(audio_file)
        logging.info(f"Pipeline finished successfully. Transcript at: {result_path}")
    except Exception as exc:
        logging.error(f"Pipeline terminated with error: {exc}")
    logging.info("Script execution ended")
