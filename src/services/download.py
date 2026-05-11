"""
DownloadService - Servico de download de midia.

Integra yt-dlp para fazer download de videos e audios do YouTube.
"""

import os
import shutil
from collections.abc import Callable
from datetime import datetime
from pathlib import Path

import yt_dlp

from src.core import get_logger
from src.models import DownloadTask, MediaMetadata, MediaType
from src.services.filesystem import FileSystemService

logger = get_logger(__name__)

WINDOWS_FFMPEG_CANDIDATES = (
    Path("C:/ffmpeg-8.1.1-essentials_build/bin"),
    Path("C:/ffmpeg/bin"),
)


class DownloadService:
    """Servico de download integrado com yt-dlp."""

    def __init__(self, fs_service: FileSystemService) -> None:
        """
        Inicializa o servico de download.

        Args:
            fs_service: Instancia de FileSystemService.
        """
        self.fs_service = fs_service
        self.progress_callback: Callable[[DownloadTask], None] | None = None

    def set_progress_callback(self, callback: Callable[[DownloadTask], None]) -> None:
        """
        Define o callback para atualizacoes de progresso.

        Args:
            callback: Funcao que recebe DownloadTask.
        """
        self.progress_callback = callback

    def extract_metadata(self, url: str) -> MediaMetadata | None:
        """
        Extrai metadados de um video.

        Args:
            url: URL do video.

        Returns:
            MediaMetadata ou None se falhar.
        """
        try:
            with yt_dlp.YoutubeDL({"quiet": True}) as ydl:
                info = ydl.extract_info(url, download=False)

                return MediaMetadata(
                    title=info.get("title", "Unknown"),
                    duration=info.get("duration", 0),
                    uploader=info.get("uploader", "Unknown"),
                    upload_date=info.get("upload_date"),
                    thumbnail_url=info.get("thumbnail", ""),
                    video_id=info.get("id", ""),
                    view_count=info.get("view_count"),
                    like_count=info.get("like_count"),
                )
        except yt_dlp.utils.DownloadError as error:
            logger.error(f"Erro do yt-dlp ao extrair metadados de {url}: {error}")
            return None
        except Exception as error:
            logger.error(f"Erro ao extrair metadados de {url}: {error}")
            return None

    def download_audio(self, url: str, task: DownloadTask) -> Path | None:
        """
        Baixa audio de um video (MP3).

        Args:
            url: URL do video.
            task: DownloadTask para rastrear progresso.

        Returns:
            Path do arquivo salvo, ou None se falhar.
        """
        ffmpeg_location = self._get_ffmpeg_location()
        return self._download_media(
            url,
            task,
            format_spec="bestaudio/best",
            ext="mp3",
            ffmpeg_location=ffmpeg_location,
        )

    def download_video(self, url: str, task: DownloadTask) -> Path | None:
        """
        Baixa video (MP4 melhor qualidade).

        Args:
            url: URL do video.
            task: DownloadTask para rastrear progresso.

        Returns:
            Path do arquivo salvo, ou None se falhar.
        """
        ffmpeg_location = self._get_ffmpeg_location()
        format_spec = (
            "bv*[ext=mp4]+ba[ext=m4a]/b[ext=mp4]/best" if ffmpeg_location else "b[ext=mp4]/best"
        )
        return self._download_media(
            url,
            task,
            format_spec=format_spec,
            ext="mp4",
            ffmpeg_location=ffmpeg_location,
        )

    def _download_media(
        self,
        url: str,
        task: DownloadTask,
        format_spec: str,
        ext: str,
        ffmpeg_location: Path | None,
    ) -> Path | None:
        """
        Faz download de midia com yt-dlp.

        Args:
            url: URL do video.
            task: DownloadTask para rastrear progresso.
            format_spec: Especificacao de formato para yt-dlp.
            ext: Extensao do arquivo.
            ffmpeg_location: Diretorio do FFmpeg, se encontrado.

        Returns:
            Path do arquivo salvo, ou None se falhar.
        """
        try:
            metadata = self.extract_metadata(url)
            if not metadata:
                logger.error(f"Falha ao extrair metadados de {url}")
                return None

            output_dir = (
                self.fs_service.audio_dir
                if task.media_type == MediaType.AUDIO
                else self.fs_service.video_dir
            )
            started_at = datetime.now().timestamp()

            ydl_opts = {
                "format": format_spec,
                "outtmpl": str(output_dir / "%(title)s.%(ext)s"),
                "quiet": True,
                "no_warnings": True,
                "merge_output_format": "mp4",
                "postprocessors": self._get_postprocessors(task.media_type, ffmpeg_location),
                "progress_hooks": [lambda data: self._progress_hook(data, task, metadata)],
            }
            if ffmpeg_location:
                ydl_opts["ffmpeg_location"] = str(ffmpeg_location)

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                filename = ydl.prepare_filename(info)
                file_path = self._resolve_downloaded_file(
                    output_dir=output_dir,
                    prepared_filename=Path(filename),
                    ext=ext,
                    started_at=started_at,
                )

                logger.info(f"Download concluido: {file_path}")
                return file_path

        except yt_dlp.utils.DownloadError as error:
            logger.error(f"Erro do yt-dlp ao baixar midia de {url}: {error}")
            return None
        except Exception as error:
            logger.error(f"Erro ao baixar midia de {url}: {error}")
            return None

    def _get_postprocessors(
        self, media_type: MediaType, ffmpeg_location: Path | None
    ) -> list[dict]:
        """
        Define os pos-processadores de acordo com o tipo de midia.

        Args:
            media_type: Tipo de midia.

        Returns:
            Lista de configuracoes de pos-processadores.
        """
        postprocessors = []

        if media_type == MediaType.AUDIO and ffmpeg_location:
            postprocessors.append(
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "192",
                }
            )

        return postprocessors

    def _get_ffmpeg_location(self) -> Path | None:
        """
        Localiza o FFmpeg para o yt-dlp.

        Returns:
            Diretorio do executavel ffmpeg, ou None se nao encontrado.
        """
        configured_location = self._get_configured_ffmpeg_location()
        if configured_location:
            return configured_location

        executable = shutil.which("ffmpeg")
        if not executable:
            discovered_location = self._discover_windows_ffmpeg_location()
            if discovered_location:
                return discovered_location

            logger.warning("FFmpeg nao encontrado no PATH do processo")
            return None

        ffmpeg_path = Path(executable)
        logger.debug(f"FFmpeg localizado em: {ffmpeg_path}")
        return ffmpeg_path.parent

    def _get_configured_ffmpeg_location(self) -> Path | None:
        """Le FFMPEG_LOCATION/FFMPEG_BINARY quando configurado pelo usuario."""
        for variable_name in ("FFMPEG_LOCATION", "FFMPEG_BINARY"):
            raw_value = os.environ.get(variable_name)
            if not raw_value:
                continue

            configured_path = Path(raw_value)
            if configured_path.is_file() and configured_path.name.lower() == "ffmpeg.exe":
                logger.info(f"FFmpeg localizado por {variable_name}: {configured_path}")
                return configured_path.parent

            if self._has_ffmpeg_executable(configured_path):
                logger.info(f"FFmpeg localizado por {variable_name}: {configured_path}")
                return configured_path

        return None

    def _discover_windows_ffmpeg_location(self) -> Path | None:
        """Procura FFmpeg em instalacoes comuns no Windows."""
        candidates = list(WINDOWS_FFMPEG_CANDIDATES)
        candidates.extend(Path("C:/").glob("ffmpeg*/bin"))

        for candidate in candidates:
            if self._has_ffmpeg_executable(candidate):
                logger.info(f"FFmpeg localizado automaticamente em: {candidate}")
                return candidate

        return None

    def _has_ffmpeg_executable(self, directory: Path) -> bool:
        """Verifica se um diretorio possui ffmpeg executavel."""
        return (directory / "ffmpeg.exe").is_file() or (directory / "ffmpeg").is_file()

    def _resolve_downloaded_file(
        self,
        output_dir: Path,
        prepared_filename: Path,
        ext: str,
        started_at: float,
    ) -> Path:
        """Resolve o arquivo final gerado pelo yt-dlp e pos-processadores."""
        expected_path = output_dir / f"{prepared_filename.stem}.{ext}"
        if expected_path.exists():
            return expected_path

        recent_files = [
            file_path
            for file_path in output_dir.glob(f"*.{ext}")
            if file_path.stat().st_mtime >= started_at
        ]
        if recent_files:
            return max(recent_files, key=lambda file_path: file_path.stat().st_mtime)

        recent_files = [
            file_path
            for file_path in output_dir.iterdir()
            if file_path.is_file() and file_path.stat().st_mtime >= started_at
        ]
        if recent_files:
            return max(recent_files, key=lambda file_path: file_path.stat().st_mtime)

        return expected_path

    def _progress_hook(self, data: dict, task: DownloadTask, metadata: MediaMetadata) -> None:
        """
        Hook de progresso do yt-dlp.

        Args:
            data: Dicionario de status do yt-dlp.
            task: DownloadTask a atualizar.
            metadata: Metadados da midia.
        """
        status = data.get("status")

        if status == "downloading":
            total = data.get("total_bytes", 0) or data.get("total_bytes_estimate", 0)
            downloaded = data.get("downloaded_bytes", 0)

            if total > 0:
                task.progress_percentage = (downloaded / total) * 100
                task.current_file_size = downloaded
                task.total_file_size = total

            if self.progress_callback:
                self.progress_callback(task)

        elif status == "finished":
            task.progress_percentage = 100.0
            if self.progress_callback:
                self.progress_callback(task)

    def is_playlist(self, url: str) -> bool:
        """
        Verifica se a URL e uma playlist.

        Args:
            url: URL a verificar.

        Returns:
            True se for playlist, False caso contrario.
        """
        try:
            with yt_dlp.YoutubeDL({"extract_flat": "in_playlist", "quiet": True}) as ydl:
                info = ydl.extract_info(url, download=False)
                return "entries" in info and info.get("_type") == "playlist"
        except Exception:
            return False
