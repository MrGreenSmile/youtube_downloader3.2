from tkinter import Tk
from tkinter import Label, Entry, Button, Checkbutton, Radiobutton
from tkinter import BooleanVar, StringVar
from tkinter.ttk import Progressbar
import threading

import os, re
import urllib.request
#from pytube import YouTube
from pytubefix import YouTube
from moviepy.editor import AudioFileClip
import directory_setter


window = Tk()
window.title('youtube-downloader 3.2.0')
window.iconbitmap('./icon.ico')

w_width = 350
w_height = 200
s_width = window.winfo_screenwidth()
s_height = window.winfo_screenheight()
width = s_width/2 - w_width/2
height = s_height/2 - w_height/2
window.geometry('%dx%d+%d+%d' % (w_width, w_height, width, height))
window.resizable(False, False)


def downloader():
    audio_dir = './audio/'
    video_dir = './video/'
    url = url_in.get()
    yt = YouTube(url)

    def thumbnailor(yt_module, diractory):
        re_subed = re.sub(r'[:?|/"]', '', yt_module.title)
        #thumb_url = yt_module.thumbnail_url.replace('sddefault', 'maxresdefault')
        thumb_url = yt.thumbnail_url.replace('720', '1080')
        thumb_name = diractory + '/thumbnail/' + re_subed + '.jpg'
        urllib.request.urlretrieve(thumb_url, thumb_name)


    if mp4ormp3.get() == 'mp3':
        def MP4toMP3(file):
            file_name = os.path.splitext(file)
            converted = AudioFileClip(file)
            converted.write_audiofile(file_name[0] + '.mp3')
            converted.close()

            os.remove(file)

        video = yt.streams.get_audio_only()
        video.download(audio_dir)
        prgbar.step(50)         ############
        
        if onlyThumb:
            thumbnailor(yt, audio_dir)
            prgbar.step(70)     ############
        print('download done.')

        videos = os.listdir(audio_dir)
        for video in videos:
            if '.mp4' in video:
                MP4toMP3(audio_dir + '/' + video)
                prgbar.step(90) ############

        print('transformation done.')
    if mp4ormp3.get() == 'mp4':
        video = yt.streams.filter(file_extension='mp4').order_by('resolution').last() #filter(progressive=True, file_extension='mp4').order_by('resolution').first()
        video.download(video_dir)

        prgbar.step(70)         ############

        if onlyThumb:
            thumbnailor(yt, video_dir)

            prgbar.step(90)     ############

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
    print('keywords : ', yt.keywords)
    print('thumbnail : ', yt.thumbnail_url)

    print('all done!')
    prgbar.step(100)            ############

    out_title = Label(window, text=yt.title, width=30, anchor='w')
    out_length = Label(window, text=str(round(yt.length/60)) + ':' + sec, width=30, anchor='w')
    out_upload = Label(window, text=yt.author, width=30, anchor='w')
    out_date = Label(window, text=str(yt.publish_date), width=30, anchor='w')
    out_title.grid(row=1, column=1)
    out_length.grid(row=2, column=1)
    out_upload.grid(row=3, column=1)
    out_date.grid(row=4, column=1)
    prgbar.stop()               ############

def threador():
    thread = threading.Thread(target=downloader)
    thread.daemon = True
    thread.start()



url_lbl = Label(window, text="url : ", width=7, anchor='w')
url_in = Entry(window, width=30)
btn = Button(window, text="여!", width=10, command=threador)
url_lbl.grid(row=0, column=0)
url_in.grid(row=0, column=1)
btn.grid(row=0, column=2)

mp4ormp3 = StringVar()
only_mp4 = Radiobutton(window, text='MP4', variable=mp4ormp3, value='mp4')
only_mp4.select()
only_mp4.grid(row=1, column=2, sticky='w')
only_audio = Radiobutton(window, text='MP3', variable=mp4ormp3, value='mp3')
only_audio.grid(row=2, column=2, sticky='w')
onlyThumb = BooleanVar()
only_thumb = Checkbutton(window, text='thumbnail', variable=onlyThumb)
only_thumb.select()
only_thumb.grid(row=3, column=2, sticky='w')

lbl1 = Label(window, text='title : ', width=7, anchor='w')
lbl2 = Label(window, text='time : ', width=7, anchor='w')
lbl3 = Label(window, text='channel : ', width=7, anchor='w')
lbl4 = Label(window, text='date : ', width=7, anchor='w')
lbl1.grid(row=1, column=0)
lbl2.grid(row=2, column=0)
lbl3.grid(row=3, column=0)
lbl4.grid(row=4, column=0)

prgbar = Progressbar(window, maximum=100, length=200)
prgbar.grid(row=6, columnspan=3)

window.mainloop()
