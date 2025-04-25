import os
import logging
from dotenv import load_dotenv
from groq import Groq

def init_env():
    load_dotenv()
    key = os.getenv("GROQ_API_KEY")
    if not key:
        logging.error("GROQ_API_KEY not found in environment.")
        raise RuntimeError("Please set GROQ_API_KEY in your environment or .env file.")
    return key

os.makedirs('text-data', exist_ok=True)
os.makedirs('summarised-data', exist_ok=True)
os.makedirs('logs', exist_ok=True)

logging.basicConfig(
    filename=os.path.join('logs', 'summarization.log'),
    filemode='a',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logging.info("Starting summarization pipeline")

groq_key = init_env()
client = Groq(api_key=groq_key)


MODEL = 'llama3-8b-8192'  
TEMPERATURE = 0.3
MAX_TOKENS = 150


def summarize_text(text: str) -> str:
    """
    Sends a chunk of transcript text to Groq and returns its summary.
    """
    logging.info("Sending text to summarization model")
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": "You are a concise and accurate summarizer. You just have to summarize the text."},
            {"role": "user",   "content": text}
        ],
        max_tokens=MAX_TOKENS,
        temperature=TEMPERATURE
    )
    summary = response.choices[0].message.content
    logging.info("Received summary from model")
    return summary


def process_files():
    """
    Iterate over each transcript in 'text-data', summarize, and save summary to 'summarised-data'.
    """
    files = [f for f in os.listdir('text-data') if f.lower().endswith('.txt')]
    if not files:
        logging.error("No transcript files found in 'text-data' folder.")
        return

    for fname in files:
        infile = os.path.join('text-data', fname)
        base = os.path.splitext(fname)[0]
        try:
            logging.info(f"Reading transcript: {infile}")
            with open(infile, 'r', encoding='utf-8') as rf:
                content = rf.read()

            summary = summarize_text(content)

            out_file = os.path.join('summarised-data', f"{base}_summary.txt")
            with open(out_file, 'w', encoding='utf-8') as wf:
                wf.write(summary)

            logging.info(f"Summary saved to: {out_file}")
        except Exception as e:
            logging.error(f"Error processing {infile}: {e}")


if __name__ == '__main__':
    logging.info("Running summarization main")
    process_files()
    logging.info("Summarization pipeline completed")
