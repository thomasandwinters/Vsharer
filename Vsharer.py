import urllib.request
import shutil
import subprocess


url = input()
if not ".json" in url:
    url += ".json"


req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
url_bytes = urllib.request.urlopen(req).read()

html = url_bytes.decode("utf8")

video_pos_buffer = 16
video_fallback_pos = html.find("fallback_url") + video_pos_buffer
video_fallback_pos_final = html.find(",", video_fallback_pos)
video_backup_link = html[video_fallback_pos:video_fallback_pos_final-1]

audio_backup_pos = video_backup_link.find("DASH")
audio_backup_link = video_backup_link[0:audio_backup_pos] + "DASH_audio.mp4"

print(video_backup_link)
print(audio_backup_link)

# buffer to go to the start of the url

video_file_name = "testDownloadVideo.mp4"
audio_file_name = "testDownloadAudio.mp4"

with urllib.request.urlopen(video_backup_link) as response, open(video_file_name, 'wb') as out_file:
    shutil.copyfileobj(response, out_file)

try:
    with urllib.request.urlopen(audio_backup_link) as response, open(audio_file_name, 'wb') as out_file:
        shutil.copyfileobj(response, out_file)
    cmd = 'C:/ffmpeg/bin/ffmpeg -i testDownloadAudio.mp4 -i testDownloadVideo.mp4 -c copy output.mp4'
    
except :
    cmd = 'C:/ffmpeg/bin/ffmpeg -i testDownloadVideo.mp4 -c copy output.mp4'
#with urllib.request.urlopen(audio_backup_link) as response, open(audio_file_name, 'wb') as out_file:
#    shutil.copyfileobj(response, out_file)

#cmd = 'C:/ffmpeg/bin/ffmpeg -i testDownloadAudio.mp4 -i testDownloadVideo.mp4 -c copy output.mp4'
subprocess.call(cmd, shell=True)

