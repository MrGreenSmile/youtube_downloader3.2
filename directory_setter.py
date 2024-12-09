import os

if not os.path.isdir('./audio') or not os.path.isdir('./video'):
    os.mkdir('./audio')
    os.mkdir('./audio/thumbnail')
    os.mkdir('./video')
    os.mkdir('./video/thumbnail')