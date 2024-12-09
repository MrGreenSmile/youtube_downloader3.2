import os, re
import sys

from pytube import YouTube
from moviepy.editor import AudioFileClip
import urllib.request


audio_dir = './audio/'
video_dir = './video/'
modes = sys.argv[1]
url = sys.argv[2]

yt = YouTube(url)

if modes == 'audio' or modes == 'a':
    def MP4toMP3(file):
        file_name = os.path.splitext(file)
        converted = AudioFileClip(file)
        converted.write_audiofile(file_name[0] + '.mp3')
        converted.close()

        os.remove(file)

    video = yt.streams.get_audio_only()
    video.download(audio_dir)

    re_subed = re.sub(r'[:?|/"]', '', yt.title)
    #thumb_url = yt.thumbnail_url.replace('sddefault', 'maxresdefault')
    thumb_url = yt.thumbnail_url.replace('720', '1080')
    thumb_name = audio_dir + '/thumbnail/' + re_subed + '.jpg'
    urllib.request.urlretrieve(thumb_url, thumb_name)
    print('download done.')

    videos = os.listdir(audio_dir)
    for video in videos:
        if '.mp4' in video:
            MP4toMP3(audio_dir + '/' + video)
    print('transformation done.')


if modes == 'video' or modes == 'v':
    video = yt.streams.get_highest_resolution()
    video.download(video_dir)

    re_subed = re.sub(r'[:?|/"]', '', yt.title)
    #thumb_url = yt.thumbnail_url.replace('sddefault', 'maxresdefault')
    thumb_url = yt.thumbnail_url.replace('720', '1080')
    thumb_name = video_dir + '/thumbnail/' + re_subed + '.jpg'
    urllib.request.urlretrieve(thumb_url, thumb_name)
    print('download done.')


if(yt.length%60 < 10):
    sec = '0' + str(yt.length%60)
if(yt.length%60 >= 10):
    sec = str(yt.length%60)

print('title : ', yt.title)
print('length : ', round(yt.length/60), ':', sec)
print('author : ', yt.author)
print('published : ', yt.publish_date)
print('views : ', yt.views)
#print('keywords : ', yt.keywords)
print('thumbnail : ', yt.thumbnail_url)

print('all done!')