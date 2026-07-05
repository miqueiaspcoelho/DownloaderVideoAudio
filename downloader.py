import os
from pathlib import Path

from yt_dlp import YoutubeDL
from yt_dlp.utils import DownloadError


class YoutubeDownloader:
    def __init__(self, url: str, playlist: bool):
        self.url = url
        self.playlist = playlist

        self.base_path = Path.home() / "Downloads"
        self.video_path = self.base_path / "videos"
        self.audio_path = self.base_path / "audios"

        os.makedirs(self.video_path, exist_ok=True)
        os.makedirs(self.audio_path, exist_ok=True)

    def _base_options(self):
        return {
            "noplaylist": not self.playlist,
            "verbose": True,

            # Necessario para o YouTube atual resolver desafios JS
            "js_runtimes": {
                "deno": {}
            },
            "remote_components": {
                "ejs:github"
            },
        }

    def videoDownload(self):
        videoOptions = self._base_options()
        videoOptions.update({
            "format": "bv*+ba/b",
            "outtmpl": str(self.video_path / "%(title)s.%(ext)s"),
            "merge_output_format": "mp4",
        })

        try:
            print("Download do video em andamento...")
            with YoutubeDL(videoOptions) as ydl:
                ydl.download([self.url])
            print("Download concluido.")
        except DownloadError as e:
            print(f"Erro no download: {e}")
        except Exception as e:
            print(f"Erro inesperado: {e}")

    def audioDownload(self):
        audioOptions = self._base_options()
        audioOptions.update({
            "format": "bestaudio/best",
            "outtmpl": str(self.audio_path / "%(title)s.%(ext)s"),
            "postprocessors": [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }],
            "prefer_ffmpeg": True,
            "keepvideo": False,
        })

        try:
            print("Download do audio em andamento...")
            with YoutubeDL(audioOptions) as ydl:
                ydl.download([self.url])
            print("Download concluido.")
        except DownloadError as e:
            print(f"Erro no download: {e}")
        except Exception as e:
            print(f"Erro inesperado: {e}")