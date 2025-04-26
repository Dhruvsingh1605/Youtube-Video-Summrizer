## Introduction

This project provides an end-to-end pipeline to:

1. **Download** audio from a YouTube video.
2. **Transcribe** the audio into text using Groq’s Whisper-compatible ASR.
3. **Summarize** the transcript using Groq’s LLM.
4. **Track** data dependencies and outputs with DVC for reproducibility.  

A future iteration will wrap this pipeline into a **Flask** web application, providing a web-based UI for users to submit YouTube URLs and retrieve summaries directly in their browser.

---

## Tech Stack & Tools

- **Python 3.8+**: Language for all scripts.  
- **yt-dlp**: Download audio streams from YouTube.  
- **FFmpeg**: Audio extraction and optional compression.  
- **Groq Python SDK**: Transcription & chat completions (via Whisper & LLM endpoints).  
- **python-dotenv**: Manage environment variables (GROQ_API_KEY).  
- **DVC**: Define and reproduce pipeline stages (`dvc.yaml`, `dvc repro`).  
- **DVC Remote**: Cloud or local storage for caching large audio/text artifacts.  
- **Logging**: Python’s `logging` module writes events to `logs/` for debugging and audit.  
- **Flask** (upcoming): Web framework to serve the pipeline as a REST API and web UI.

---

## Project Structure

```
├── data/                  # Raw and intermediate audio files
│   └── downloaded_audio.wav
├── text-data/             # Raw transcript text files
│   └── downloaded_audio.txt
├── summarised-data/       # Final summary text files
│   └── downloaded_audio_summary.txt
├── logs/                  # Pipeline execution logs
│   ├── Audio-to-Text.log
│   └── summarization.log
├── src/                   # Python scripts
│   ├── Youtube_Audio.py   # Download & extract audio
│   ├── Audio-text.py      # Transcribe audio → text
│   └── Summarization.py   # Summarize transcript
├── dvc.yaml               # DVC pipeline definition
├── .dvc/config            # DVC remote configuration
├── .env                   # Environment variables (e.g., GROQ_API_KEY)
└── README.md              # This documentation
```

---

## Setup & Installation

1. **Clone the repo**:
   ```bash
   git clone <repo-url>
   cd <repo-directory>
   ```

2. **Install dependencies**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Install FFmpeg** (system-wide or bundle):
   - macOS: `brew install ffmpeg`
   - Ubuntu: `sudo apt install ffmpeg`
   - Windows: download static build, add to PATH

4. **Configure environment**:
   ```bash
   cp .env.example .env
   # edit .env to add GROQ_API_KEY
   ```

5. **Configure DVC remote** (optional):
   ```bash
   dvc remote add -d storage s3://my-bucket/dvc-cache
   ```

6. **Reproduce the pipeline**:
   ```bash
   dvc pull     # fetch cached data
   dvc repro    # run missing stages
   ```

---

## Usage

To run the full pipeline manually:

```bash
python3 src/Youtube_Audio.py "https://www.youtube.com/watch?v=<VIDEO_ID>"
python3 src/Audio-text.py
python3 src/Summarization.py
```  
Or simply:  
```bash
dvc repro
```

Outputs:
- **Raw audio**: `data/downloaded_audio.wav`  
- **Transcript**: `text-data/downloaded_audio.txt`  
- **Summary**: `summarised-data/downloaded_audio_summary.txt`

---

## Future Work

- **Flask Web App**:
  - Expose REST endpoints: `/download`, `/transcribe`, `/summarize`  
  - Simple front-end form to submit YouTube URLs and display summaries  
  - Deployable via Docker or cloud services

- **Improvements**:
  - Dynamic chunking and real-time progress updates  
  - User authentication and history tracking  
  - Support for additional languages and models

---

## Contributing & License

Contributions are welcome! Please open issues or pull requests.  
This project is licensed under the MIT License.

