import urllib.request
import shutil
import ffmpy3
import json

# Crudely set up the URL
# This needs more checks
print("Input URL: ", end='')
url = input()
if not ".json" in url:
    url += ".json"

# General the URL request and get the JSON
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
url_bytes = urllib.request.urlopen(req).read()

html = url_bytes.decode("utf8")

# Load JSON
page_json = json.loads(html)

# Get the backup link for the video from JSON
video_backup_link = page_json[0]["data"]["children"][0]["data"]["secure_media"]["reddit_video"]["fallback_url"]

# Create the audio backup link by replacing everything after "DASH" in the video URL with "_audio.mp4"
audio_backup_pos = video_backup_link.find("DASH")
audio_backup_link = video_backup_link[0:audio_backup_pos] + "DASH_audio.mp4"

# Debug output
print(video_backup_link)
print(audio_backup_link)

# Set filenames for video and audio
video_file_name = "video.mp4"
audio_file_name = "audio.mp4"

# Request the backup video file
with urllib.request.urlopen(video_backup_link) as response, open(video_file_name, 'wb') as out_file:
    shutil.copyfileobj(response, out_file)

# Try to Request the backup audio file
try:
    with urllib.request.urlopen(audio_backup_link) as response, open(audio_file_name, 'wb') as out_file:
        shutil.copyfileobj(response, out_file)
    # If there is an audio file, encode video and audio together and outpiut as output.mp4
    ff = ffmpy3.FFmpeg(global_options="-y", inputs={video_file_name: None, audio_file_name: None}, outputs={"output.mp4": "-c:v h264 -c:a ac3"})
# If no audio exists, encode just the video as output.mp4
except:
    ff = ffmpy3.FFmpeg(global_options="-y", inputs={video_file_name: None}, outputs={"output.mp4": "-c:v h264"})

ff.run()
