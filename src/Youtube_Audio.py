import os
import logging
from yt_dlp import YoutubeDL

os.makedirs('Data', exist_ok=True)
os.makedirs('logs', exist_ok=True)


logging.basicConfig(
    filename=os.path.join('logs', 'app.log'),  
    filemode='a',                              
    level=logging.INFO,                        
    format='%(asctime)s - %(levelname)s - %(message)s'
)


def download_audio_from_youtube(url: str) -> str:
    """
    Downloads best-quality audio and returns the local filename.
    Also logs each step into the 'app.log' file inside 'logs/'.
    """
    logging.info(f"Starting download for URL: {url}")

    ydl_opts = {
        'format': 'bestaudio/best',                         
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',                    
            'preferredcodec': 'wav',                        
            'preferredquality': '192',                      
        }],
        'outtmpl': 'Data/downloaded_audio.%(ext)s',         
    }
    try:
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            wav_path = ydl.prepare_filename(info).replace(info['ext'], 'wav')
        logging.info(f"Download and conversion successful. Saved to: {wav_path}")
        return wav_path

    except Exception as e:
        logging.error(f"Error downloading audio from {url}: {e}")
        raise


if __name__ == "__main__":
    test_url = "https://www.youtube.com/watch?v=FAyKDaXEAgc"
    logging.info("Script execution started")
    try:
        output_file = download_audio_from_youtube(test_url)
        logging.info(f"Script completed successfully, output: {output_file}")
    except Exception:
        logging.error("Script terminated with errors")
    logging.info("Script execution ended")
