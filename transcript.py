import json
import yt_dlp
import whisper
import os
import logging
import ssl
import re
import sys
import time
import random
import string

ssl._create_default_https_context = ssl._create_unverified_context

# Record the start time
start_time = time.time()

# You can adjust the model used here. Model choice is typically a tradeoff between accuracy and speed.
# All available models are located at https://github.com/openai/whisper/#available-models-and-languages.
#whisper_model = whisper.load_model("base")
whisper_model = whisper.load_model("medium", download_root="/Users/lequang/Documents/Project/Website/PHP7/ai.fourelementscorp.com/python_app/build")


def save_to_file(name, content):
    # Open a file in write mode ('w')
    with open(f'file/{name}.json', 'w', encoding="utf-8") as file:
        # Write some text to the file
        file.write(content)

def get_video_title(video_url):
    options = {
        'quiet': True,
    }

    with yt_dlp.YoutubeDL(options) as ydl:
        info_dict = ydl.extract_info(video_url, download=False)
        video_title = info_dict.get('title', None)

    return video_title

def get_youtube_video_id(url):
    pattern = re.compile(r'(?:youtube\.com\/(?:[^\/\n\s]+\/\S+\/|(?:v|e(?:mbed)?)\/|\S*?[?&]v=)|youtu\.be\/)([a-zA-Z0-9_-]{11})')
    match = pattern.search(url)

    if match:
        return match.group(1)
    else:
        return None

def random_string(length=12):
    chars = string.ascii_letters + string.digits  # a-zA-Z0-9
    return ''.join(random.choices(chars, k=length))

def string_to_slug(input_string):
    # Remove leading and trailing whitespaces
    input_string = input_string.strip()

    # Convert to lowercase
    input_string = input_string.lower()

    # Replace spaces with hyphens
    input_string = re.sub(r'\s+', '-', input_string)

    # Remove special characters
    input_string = re.sub(r'[^a-zA-Z0-9-]', '', input_string)

    return input_string

def download(video_url) -> str:
    #video_url = f'https://www.youtube.com/watch?v={video_id}'
    ydl_opts = {
        'format': 'm4a/bestaudio/best',
        'paths': {'home': 'audio/'},
        'outtmpl': {'default': '%(id)s.%(ext)s'},
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'm4a',
        }]
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        error_code = ydl.download([video_url])
        if error_code != 0:
            raise Exception('Failed to download video')

    video_id = get_youtube_video_id(video_url)
    return f'audio/{video_id}.m4a'


def transcribe(file_path: str) -> str:
        # `fp16` defaults to `True`, which tells the model to attempt to run on GPU.
        # For local demonstration purposes, we'll run this on the CPU by setting it to `False`.
        transcription = whisper_model.transcribe(file_path, fp16=False, language="Vietnamese")
        return transcription['text']

def transcript(youtube_url):
    video_title = get_video_title(youtube_url)
    file_path = download(youtube_url)
    if file_path:
        text = transcribe(file_path)
        file_name = string_to_slug(video_title)
        os.remove(file_path)
        save_to_file(file_name, json.dumps({'text':text, 'title': video_title, 'url': youtube_url}, indent=2))
        print(f"Saved to {file_name}.json")

def transcript_file(file_path):
    text = transcribe(file_path)
    file_name = random_string(12)
    os.remove(file_path)
    save_to_file(file_name, json.dumps({'text':text, 'title': '', 'url': file_path}, indent=2))
    print(f"Saved to {file_name}.json")

# Check if the correct number of command-line arguments is provided
if len(sys.argv) != 3:
    print("Usage: python transcript.py <f | y> <file_path | youtube_url>")
    sys.exit(1)  # Exit with an error code

# Get the parameter from the command line
type = sys.argv[1]
url = sys.argv[2]
if type == 'y' :
    transcript(url)
else :
    transcript_file(url)

# Record the end time
end_time = time.time()

# Calculate the duration
duration = end_time - start_time

# Log the duration
print(f"Function took {duration:.2f} seconds to execute.")
sys.exit(0)