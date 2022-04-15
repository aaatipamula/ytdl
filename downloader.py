import yt_dlp
import os

class Downloader():
    def __init__(self, url, music_dir, video_dir):
        self.url = url
        self.music_dir = music_dir
        self.video_dir = video_dir

        with yt_dlp.YoutubeDL() as ydl:
            info = ydl.extract_info(url, download=False)
        
        self.video_title = info.get('title', None)

    def download_audio(self):
        os.chdir(self.music_dir)
        print(f"\nChanging directory to {os.getcwd()}...")

        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': '%(title)s.%(ext)s',
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
                'preferedformat':'mp4',
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