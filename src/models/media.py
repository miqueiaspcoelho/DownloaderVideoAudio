"""
Modelos de domínio para o YouTube Media Downloader.

Define estruturas de dados para representar entidades do sistema.
"""

from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from pathlib import Path


class MediaType(Enum):
    """Tipos de mídia suportados."""

    VIDEO = "video"
    AUDIO = "audio"


class DownloadStatus(Enum):
    """Status de um download."""

    PENDING = "pending"
    DOWNLOADING = "downloading"
    COMPLETED = "completed"
    FAILED = "failed"
    PAUSED = "paused"


@dataclass
class MediaMetadata:
    """Metadados de uma mídia."""

    title: str
    duration: int  # em segundos
    uploader: str
    upload_date: str | None
    thumbnail_url: str
    video_id: str
    view_count: int | None = None
    like_count: int | None = None


@dataclass
class Media:
    """Representa um vídeo ou áudio baixado."""

    file_path: Path
    media_type: MediaType
    metadata: MediaMetadata
    file_size: int  # em bytes
    downloaded_at: datetime
    thumbnail_path: Path | None = None

    def get_human_size(self) -> str:
        """Retorna o tamanho em formato legível."""
        for unit in ["B", "KB", "MB", "GB"]:
            if self.file_size < 1024.0:
                return f"{self.file_size:.2f} {unit}"
            self.file_size /= 1024.0
        return f"{self.file_size:.2f} TB"


@dataclass
class DownloadTask:
    """Representa uma tarefa de download."""

    url: str
    media_type: MediaType
    status: DownloadStatus = DownloadStatus.PENDING
    progress_percentage: float = 0.0
    current_file_size: int = 0
    total_file_size: int = 0
    error_message: str | None = None
    downloaded_media: Media | None = None
    is_playlist: bool = False
    playlist_items: int = 0
    current_item: int = 0


@dataclass
class PlaylistInfo:
    """Informações sobre uma playlist."""

    url: str
    title: str
    uploader: str
    total_videos: int
    videos: list[MediaMetadata]
