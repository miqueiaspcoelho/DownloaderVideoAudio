import os
from yt_dlp import YoutubeDL
from yt_dlp.utils import DownloadError
from pathlib import Path

class YoutubeDownloader:
    def __init__(self, url: str, playlist: bool):
        self.url = url
        self.playlist = playlist        
        self.path = Path.home() / "Downloads"
        
        os.makedirs(self.path, exist_ok=True)
    
    
    def videoDownload(self):
        videoOptions = {
            'format': 'bestvideo+bestaudio/best',
            'outtmpl': os.path.join(f"{self.path}/videos", '%(title)s.%(ext)s'),
            'merge_output_format': 'mp4',
            'noplaylist': self.playlist
        }
        try:
            with YoutubeDL(videoOptions) as ydl:
                ydl.download([self.url])
        except DownloadError as e:
            print(f"Erro no download: {e}")
        except Exception as e:
            print(f"Erro inesperado: {e}")
    
    def audioDownload(self):
        audioOptions = {
            'format': 'bestaudio/best',
            'outtmpl': os.path.join(f"{self.path}/audios", '%(title)s.%(ext)s'),
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'prefer_ffmpeg': True,
            'keepvideo': False,
            'noplaylist': self.playlist
        }
        try:
            with YoutubeDL(audioOptions) as ydl:
                ydl.download([self.url])
        except DownloadError as e:
            print(f"Erro no download: {e}")
        except Exception as e:
            print(f"Erro inesperado: {e}")