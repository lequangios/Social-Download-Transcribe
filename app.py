from flask import Flask, request, jsonify
import json
import yt_dlp
import whisper
import os
import logging
import ssl
import re

ssl._create_default_https_context = ssl._create_unverified_context

app = Flask(__name__)

# You can adjust the model used here. Model choice is typically a tradeoff between accuracy and speed.
# All available models are located at https://github.com/openai/whisper/#available-models-and-languages.
whisper_model = whisper.load_model("base")

def save_to_file(name, content):
    # Open a file in write mode ('w')
    with open(f'file/{name}.json', 'w') as file:
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


# Define a route and map it to a Python function
@app.route('/')
def home():
    return 'Hello, this is the home page!'

@app.route('/transcript', methods=['GET'])
def transcript():
    if request.args.get('youtube_url') and request.args.get('language_code'):
        youtube_url = request.args.get('youtube_url')
        language_code = request.args.get('language_code')
        whisper_model = whisper.load_model("base."+str(language_code))
        file_path = download(youtube_url)
        video_title = get_video_title(youtube_url)
        if file_path:
            text = transcribe(file_path)
            os.remove(file_path)
            save_to_file(string_to_slug(video_title), json.dumps({'text':text, 'title': video_title, 'url': youtube_url}, indent=2))
            return jsonify({'text':text}), 200
        else:
            return jsonify({'text':''}), 200
    else:
        return jsonify({'text':''}), 200

#     try:
#         if request.args.get('youtube_url') and request.args.get('language_code'):
#             return 'Hello, this is the home page!'
#
#             youtube_url = request.args.get('youtube_url')
#             language_code = request.args.get('language_code')
#             return jsonify({'youtube_url':youtube_url, 'language_code':language_code}), 200
#             whisper_model = whisper.load_model("base."+str(language_code))
#             file_path = download(youtube_url)
#             if file_path:
#                 text = transcribe(file_path)
#                 os.remove(file_path)
#                 return text, 200
#             else:
#                 return '', 200
#         else:
#             return '', 200
#     except Exception as e:
#         return "{e}", 500
#     finally:
#         return "Unknown error", 500


def transcribe(file_path: str) -> str:
        # `fp16` defaults to `True`, which tells the model to attempt to run on GPU.
        # For local demonstration purposes, we'll run this on the CPU by setting it to `False`.
        transcription = whisper_model.transcribe(file_path, fp16=False)
        return transcription['text']

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

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')