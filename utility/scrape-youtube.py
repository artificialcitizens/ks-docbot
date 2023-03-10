import whisper
import pytube
from datetime import datetime

url = "https://www.youtube.com/watch?v=20iV7caN3rc"
video = pytube.YouTube(url)
audio = video.streams.get_audio_only()
print(f'downloading video: {video.title}')
audio.download(filename='tmp.mp3') # Downloads only audio from youtube video
print(f'loading video: {video.title}')
model = whisper.load_model("small")
print(f'transcribing video: {video.title}')
transcription = model.transcribe('tmp.mp3')
res = transcription['segments']
print(res)
def store_segments(segments):
  texts = []
  start_times = []

  for segment in segments:
    text = segment['text']
    start = segment['start']

    # Convert the starting time to a datetime object
    start_datetime = datetime.fromtimestamp(start)

    # Format the starting time as a string in the format "00:00:00"
    formatted_start_time = start_datetime.strftime('%H:%M:%S')

    texts.append("".join(text))
    start_times.append(formatted_start_time)

  return texts, start_times

texts, start_times = store_segments(res)