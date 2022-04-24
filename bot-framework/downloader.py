from email.mime import base
import yt_dlp
import os
import base64

class Downloader():
    def __init__(self, url, music_dir, video_dir):
        self.url = url
        self.music_dir = music_dir
        self.video_dir = video_dir

        with yt_dlp.YoutubeDL() as ydl:
            info = ydl.extract_info(url, download=False)
        
        self.video_title = info.get('title', None)
        self.video_title_base64 = base64.urlsafe_b64encode(self.video_title.encode("utf-8"))
        self.base64_string = self.video_title_base64.decode('utf-8')

    def download_audio(self):
        os.chdir(self.music_dir)
        print(f"\nChanging directory to {os.getcwd()}...")

        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': f'{self.base64_string}.%(ext)s',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '320',
            }],
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([self.url]) 


    def download_video(self):
        os.chdir(self.video_dir)
        print(f"\nChanging directory to {os.getcwd()}...")

        ydl_opts = {
            'outtmpl':'%(title)s.%(ext)s',
            'postprocessors': [{
                'key':'FFmpegVideoConvertor',
                'preferredformat':'mp4',
                'perferredquality':'1080p'
            }],
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([self.url])

    def download_both(self):
        self.music_download()
        self.video_download()

    def switcher(self, selection):
        key = {
        "1":"audio",
        "2":"video",
        "3":"both",
        }
        method_name = f"download_{key.get(selection, '.')}"
        method = getattr(self, method_name, ".")
        return method()