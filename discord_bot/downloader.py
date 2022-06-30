import yt_dlp
import os
import base64

class Downloader():
    def __init__(self, url: str, mp3_dir :str, webm_dir :str):
        self.url = url
        self.mp3_dir = mp3_dir
        self.webm_dir = webm_dir

        with yt_dlp.YoutubeDL() as ydl:
            info = ydl.extract_info(url, download=False)
        
        self.video_title = info.get('title', None)
        self.video_title_base64 = base64.urlsafe_b64encode(self.video_title.encode("utf-8"))
        self.base64_string = self.video_title_base64.decode('utf-8')

    def download_mp3(self):
        os.chdir(self.mp3_dir)
        print(f"\nChanging directory to {os.getcwd()}...")

        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': f'{self.base64_string}.%(ext)s',
            'noplaylist':True,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '320',
            }],
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([self.url]) 


    def download_webm(self):
        os.chdir(self.webm_dir)
        print(f"\nChanging directory to {os.getcwd()}...")

        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl':f'{self.base64_string}.%(ext)s',
            'noplaylist':True,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([self.url])

    #Extraneous functions as a result of import from another project
    def download_both(self):
        self.music_download()
        self.video_download()

    def switcher(self, selection :str):
        key = {
        "1":"audio",
        "2":"video",
        "3":"both",
        }
        method_name = f"download_{key.get(selection, '.')}"
        method = getattr(self, method_name, ".")
        return method()