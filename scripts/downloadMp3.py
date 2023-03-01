import os

import yt_dlp

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))


def download(path):
    video_info = yt_dlp.YoutubeDL().extract_info(
        url=path, download=False
    )
    file_name = video_info['title']
    file_path = os.path.join(ROOT_DIR, file_name + '.mp3')

    options = {
        'format': 'bestaudio/best',
        'keepvideo': False,
        'outtmpl': os.path.join(ROOT_DIR, file_path),
    }

    with yt_dlp.YoutubeDL(options) as ydl:
        ydl.download([video_info['webpage_url']])

    return {'name': file_name, 'path': file_path}
